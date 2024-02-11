import json
import os
from utils import (
    extract_variables_with_regex,
    code_compilable,
    run_code,
    extract_function_name_and_args,
    extract_variables,
    check_function_for_state_change,
)
from code_templates import PREPEND_CODE, APPEND_CODE
from prompts import *


# the class for state transitional functions and rendering functions
class Function:
    def __init__(
        self,
        name,
        description,
        implementation,
        type=None,
        relevant_state_names=None,
    ):
        self.name = name
        self.description = description
        self._implementation = implementation
        self.relevant_state_names = relevant_state_names

        self.implementation = self._implementation

    @property
    def implementation(self):
        return self._implementation

    @implementation.setter
    def implementation(self, new_implementation):
        self._implementation = self.fix(new_implementation)

    def fix(self, new_implementation):
        return new_implementation.replace("""\\n""", "\n")

    def __str__(self):
        # extract all the lines after the first line of the implementation
        implementation = "\n".join(self.implementation.split("\n")[1:])
        return (
            f"def {self.name}(state_manager):\n"
            f'    """{self.description}"""\n'
            f"{implementation}\n"
            f" .   pass\n"
        )

    def sanity_check(self):
        function_name, args = extract_function_name_and_args(self.implementation)
        if function_name != self.name:
            return False
        if len(args) == 1:
            return str(args[0]).strip() == "state_manager"
        elif len(args) == 2:
            return (
                str(args[0]).strip() == "state_manager"
                and str(args[1]).strip() == "event"
            )
        else:
            return False


class StateVariable:
    def __init__(self, name, value, variable_type, description, dont_clean=False):
        self.name = name
        self._value = value
        self.variable_type = variable_type
        self.description = description
        self.dont_clean = dont_clean
        self.value = self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = self.fix(new_value)

    def fix(self, new_value):
        if self.variable_type == None or self.variable_type == "bool":
            if new_value == "true":
                return "True"
            if new_value == "false":
                return "False"
        if self.variable_type == "str":
            if not new_value.startswith('"') and not new_value.startswith("'"):
                return f'"""{new_value}"""'

        return new_value

    def __str__(self):
        if self.variable_type not in ["int", "float", "str", "bool", "tuple", "list"]:
            return f"# {self.description}\n" f"self.{self.name} = {self.value}\n"
        return (
            f"# {self.description}\n"
            f"self.{self.name} = {self.variable_type}({self.value})\n"
        )


class GameRep:
    def __init__(
        self, HEIGHT=600, WIDTH=800, FPS=60, log_dir=None, debug_mode=False, client=None
    ):
        self.queries = []
        # a list of states
        self.states = []
        # a list of input logics (functions)
        self.input_logics = []
        # a list of state transitional logics (functions)
        self.logics = []
        # a list of rendering functions that are called in the main loop
        self.renders = []

        # default variables
        self.states.append(
            StateVariable(
                name="SCREEN_HEIGHT",
                value=HEIGHT,
                variable_type="int",
                description="height of the gameplay screen",
                dont_clean=True
            )
        )
        self.states.append(
            StateVariable(
                name="SCREEN_WIDTH",
                value=WIDTH,
                variable_type="int",
                description="width of the gameplay screen",
                dont_clean=True
            )
        )
        self.states.append(
            StateVariable(
                name="FPS",
                value=FPS,
                variable_type="int",
                description="fps of the gameplay screen",
                dont_clean=True
            )
        )

        self.debug_mode = debug_mode
        self.log_dir = log_dir
        # create log dir if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        self.query_idx = 0
        self.num_api_calls = 0
        self.client = client

    def pass_sanity_check(self):
        for function in self.renders:
            if check_function_for_state_change(function.implementation):
                return False, "render function does not pass sanity check"

        all_code = self.export_code()
        if not code_compilable(all_code):
            return False, None

        no_condition_code = self.export_code()
        no_condition_code = no_condition_code.replace(
            "while running:", "for _ in range(300):"
        )
        # TODO: simulate user actions
        stdout, stderr = run_code(no_condition_code)
        if stderr != "":
            return False, stderr
        return True, stdout

    def log_query(self, filename, query, json_content):
        basename = os.path.basename(filename)
        parent_dir = os.path.dirname(filename)
        # parent_dir / {query_idx} / basename
        new_dir = os.path.join(parent_dir, str(self.query_idx))
        os.makedirs(new_dir, exist_ok=True)
        with open(os.path.join(new_dir, basename), "w") as f:
            f.write(query)
            f.write("\n====================\n\n")
            json.dump(json_content, f, indent=4)

    def ask_llm(self, query):
        success = False
        while not success:
            self.num_api_calls += 1
            completion = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant to a Pygame designer. Your response should be in JSON format.",
                    },
                    {
                        "role": "user",
                        "content": query,
                    },
                ],
                response_format={"type": "json_object"},
            )
            assert len(completion.choices) == 1
            try:
                responses = json.loads(completion.choices[0].message.content)
                success = True
            except:
                continue
        return responses

    def get_state_manager_code(self, relevant_states=None):
        code = "class StateManager:\n"
        code += "    def __init__(self):\n"
        if relevant_states:
            for state in relevant_states:
                for line in str(state).split("\n"):
                    code += f"        {line}\n"
        else:
            for state in self.states:
                for line in str(state).split("\n"):
                    code += f"        {line}\n"
        return code

    def get_function_def(
        self, given_functions, input_logic=False, include_implementation=False
    ):
        code = ""
        for function in given_functions:
            if input_logic:
                code += f"def {function.name}(state_manager, event):\n"
            else:
                code += f"def {function.name}(state_manager):\n"
            code += f'    """{function.description}"""\n'
            if include_implementation:
                code += "\n".join(function.implementation.split("\n")[1:]) + "\n"
            else:
                code += f"    # omitted for brevity\n"
            code += "\n"
        return code

    def decompose_query(self, query, contextual_states):
        def not_disjoint(list1, list2):
            return len(set(list1).intersection(list2)) > 0

        # if logic.states is overlappign with relevant states
        self.contextual_state_names = [state.name for state in contextual_states]
        contextual_input_logics = [
            input_logic
            for input_logic in self.input_logics
            if not_disjoint(
                self.contextual_state_names, input_logic.relevant_state_names
            )
        ]
        contextual_logics = [
            logic
            for logic in self.logics
            if not_disjoint(self.contextual_state_names, logic.relevant_state_names)
        ]
        contextual_renders = [
            render
            for render in self.renders
            if not_disjoint(self.contextual_state_names, render.relevant_state_names)
        ]
        query = decompose_query_prompt.format(
            state_manager_code=self.get_state_manager_code(contextual_states),
            relevant_input_def=self.get_function_def(
                contextual_input_logics, include_implementation=True
            ),
            relevant_logic_def=self.get_function_def(
                contextual_logics, include_implementation=True
            ),
            relevant_render_def=self.get_function_def(
                contextual_renders, include_implementation=True
            ),
            query=query,
        )
        decomposition = self.ask_llm(query)

        if self.debug_mode:
            self.log_query(
                filename=f"{self.log_dir}/decompose_{self.num_api_calls}.txt",
                query=query,
                json_content=decomposition,
            )

        return decomposition

    def add_new_function(self, existing_functions, new_functions):
        for new_function in new_functions:
            existing_function = next(
                (
                    function
                    for function in existing_functions
                    if function.name == new_function.name
                ),
                None,
            )
            if existing_function:
                existing_function.description = new_function.description
                existing_function.implementation = new_function.implementation
                existing_function.relevant_state_names = (
                    new_function.relevant_state_names
                )
            else:
                existing_functions.append(new_function)

    def process_user_query(self, query):
        self.queries.append({"query": query})
        yield f"processing your query... {query}"
        original_states = self.states.copy()
        original_input_logics = self.input_logics.copy()
        original_logics = self.logics.copy()
        original_renders = self.renders.copy()

        pass_check = False
        while not pass_check:
            self.states = original_states
            self.input_logics = original_input_logics
            self.logics = original_logics
            self.renders = original_renders

            # decompose query into actions
            contextual_states = self.state_change(query)
            # get the values of the dict contextual_states
            contextual_states = list(contextual_states.values())
            yield "extracting subgraph ..."
            actions = self.decompose_query(query, contextual_states)
            if actions.keys() != {"input_logic", "state_transition", "ui_rendering"}:
                continue

            try:
                function_description = actions["input_logic"]["description"]
                function_name = actions["input_logic"]["function_name"]
                if not (function_name == "" or function_description == ""):
                    yield f"implementing {function_name} ..."
                    yield f"{function_description}"
                    self.input_logics = [
                        function
                        for function in self.input_logics
                        if function.name != function_name
                    ]
                    input_logics = self.input_logic_add(
                        function_name, function_description, contextual_states
                    )
                    self.queries[-1]["input_logic"] = [
                        logic.name for logic in input_logics
                    ]
                    self.add_new_function(self.input_logics, input_logics)

                function_description = actions["state_transition"]["description"]
                function_name = actions["state_transition"]["function_name"]
                if not (function_name == "" or function_description == ""):
                    yield f"implementing {function_name} ..."
                    yield f"{function_description}"
                    self.logics = [
                        function
                        for function in self.logics
                        if function.name != function_name
                    ]
                    logics = self.logic_add(
                        function_name, function_description, contextual_states
                    )
                    self.queries[-1]["logic"] = [logic.name for logic in logics]
                    self.add_new_function(self.logics, logics)

                function_description = actions["ui_rendering"]["description"]
                function_name = actions["ui_rendering"]["function_name"]
                if not (function_name == "" or function_description == ""):
                    yield f"implementing {function_name} ..."
                    yield f"{function_description}"
                    self.renders = [
                        function
                        for function in self.renders
                        if function.name != function_name
                    ]
                    renders = self.ui_add(
                        function_name, function_description, contextual_states
                    )
                    self.queries[-1]["rendering"] = [logic.name for logic in renders]
                    self.add_new_function(self.renders, renders)
            except:
                continue

            self.clean_states()
            if self.debug_mode:
                print("number of state variables", len(self.states))

            all_code = self.export_code()
            save_path = f"{self.log_dir}/{self.query_idx}/{self.num_api_calls}_final.py"
            with open(save_path, "w") as f:
                f.write(all_code)

            pass_check, error_trace = self.pass_sanity_check()
            if pass_check:
                yield "pass sanity check."
            else:
                yield "fail sanity check."
                yield error_trace

        save_path = f"{self.log_dir}/{self.query_idx}/final.py"
        with open(save_path, "w") as f:
            f.write(all_code)
        self.query_idx += 1

    def clean_states(self):
        # the first 3 are the default states
        used_states = {state.name: False for state in self.states}
        for state in self.states:
            if state.dont_clean:
                used_states[state.name] = True

        all_vars = []
        for state in self.states:
            if state.variable_type == "str":
                all_vars.extend(extract_variables(state.value))
        for var in all_vars:
            if var in used_states.keys():
                used_states[var] = True

        for function in self.input_logics + self.logics + self.renders:
            for state_name in function.relevant_state_names:
                used_states[state_name] = True
        self.states = [state for state in self.states if used_states[state.name]]

    def state_change(self, query):
        query = state_change_prompt.format(
            state_manager_code=self.get_state_manager_code(), query=query
        )
        while True:
            _new_states = self.ask_llm(query)
            if self.debug_mode:
                self.log_query(
                    filename=f"{self.log_dir}/state_{self.num_api_calls}.txt",
                    query=query,
                    json_content=_new_states,
                )

            new_states = _new_states["state_variables"]
            # if any state has the value of [], retry
            if any(state["variable_value"] == "[]" for state in new_states):
                continue
            for state in new_states:
                if state["variable_type"] == "str":
                    if not state["variable_value"].startswith('"') and not state["variable_value"].startswith("'"):
                        state["variable_value"] = f'"""{state["variable_value"]}"""'
            # make sure the variable_value does not contain other variables
            if any(
                len(extract_variables(state["variable_value"])) > 0
                for state in new_states
            ):
                continue

            ret_new_states = dict()
            for state in self.states:
                if state.dont_clean:
                    ret_new_states[state.name] = state
                
            for state in new_states:
                existing_state = next(
                    (s for s in self.states if s.name == state["variable_name"]), None
                )
                if existing_state:
                    existing_state.value =state["variable_value"]
                    ret_new_states[existing_state.name] = existing_state
                else:
                    _new_state = StateVariable(
                        name=state["variable_name"],
                        value=state["variable_value"],
                        variable_type=state["variable_type"],
                        description=state["variable_description"],
                    )
                    self.states.append(_new_state)
                    ret_new_states[state["variable_name"]] = _new_state

            return ret_new_states

    def input_logic_add(
        self, function_name, function_description, relevant_states=None
    ):
        # if the function_name exists in self.input_logics, existing_implementation should be set
        existing_implementation = next(
            (
                function.implementation
                for function in self.input_logics
                if function.name == function_name
            ),
            "",
        )

        query = input_logic_add_prompt.format(
            state_manager_code=self.get_state_manager_code(relevant_states),
            existing_implementation=existing_implementation,
            function_name=function_name,
            function_description=function_description,
        )
        while True:
            input_logic = self.ask_llm(query)
            if self.debug_mode:
                self.log_query(
                    filename=f"{self.log_dir}/input_logic_{self.num_api_calls}.txt",
                    query=query,
                    json_content=input_logic,
                )

            new_functions = [
                Function(
                    name=input_logic["function_name"],
                    description=input_logic["function_description"],
                    implementation=input_logic["function_implementation"],
                    type="input_logic",
                    relevant_state_names=extract_variables_with_regex(
                        input_logic["function_implementation"], keyword="state_manager"
                    ),
                )
            ]

            retry = False
            # function should not use any state that is not defined
            for function in new_functions:
                if not all(
                    state_name in self.contextual_state_names
                    for state_name in function.relevant_state_names
                ):
                    retry = True
            if retry:
                continue

            # if all functions pass basic sanity check
            if all([function.sanity_check() for function in new_functions]):
                return new_functions

    def logic_add(self, function_name, function_description, relevant_states=None):
        # if the function_name exists in self.input_logics, existing_implementation should be set
        existing_implementation = next(
            (
                function.implementation
                for function in self.logics
                if function.name == function_name
            ),
            "",
        )

        query = logic_add_prompt.format(
            state_manager_code=self.get_state_manager_code(relevant_states),
            existing_implementation=existing_implementation,
            function_name=function_name,
            function_description=function_description,
        )
        while True:
            logic = self.ask_llm(query)
            if self.debug_mode:
                self.log_query(
                    filename=f"{self.log_dir}/logic_{self.num_api_calls}.txt",
                    query=query,
                    json_content=logic,
                )

            new_functions = [
                Function(
                    name=logic["function_name"],
                    description=logic["function_description"],
                    implementation=logic["function_implementation"],
                    type="logic",
                    relevant_state_names=extract_variables_with_regex(
                        logic["function_implementation"], keyword="state_manager"
                    ),
                )
            ]
            # if all functions pass basic sanity check
            if all([function.sanity_check() for function in new_functions]):
                return new_functions

    def ui_add(self, function_name, function_description, relevant_states=None):
        query = ui_add_prompt.format(
            function_name=function_name,
            function_description=function_description,
            state_manager_code=self.get_state_manager_code(relevant_states),
            render_code="\n".join([render.implementation for render in self.renders]),
        )
        while True:
            render = self.ask_llm(query)
            if self.debug_mode:
                self.log_query(
                    filename=f"{self.log_dir}/render_{self.num_api_calls}.txt",
                    query=query,
                    json_content=render,
                )

            # when you change the value of a state, you need to potentially modify existing logics
            new_functions = [
                Function(
                    name=render["function_name"],
                    description=render["function_description"],
                    implementation=render["function_implementation"],
                    type="render",
                    relevant_state_names=extract_variables_with_regex(
                        render["function_implementation"], keyword="state_manager"
                    ),
                )
            ]

            if all([function.sanity_check() for function in new_functions]):
                return new_functions

    def export_code(self):
        all_code = PREPEND_CODE
        # add StateManager
        all_code += self.get_state_manager_code()

        for input_logic in self.input_logics:
            all_code += input_logic.implementation + "\n\n"

        for logic in self.logics:
            all_code += logic.implementation + "\n\n"

        for render in self.renders:
            all_code += render.implementation + "\n\n"

        input_logic_code = ""
        for function in self.input_logics:
            input_logic_code += f"        # {function.description}\n"
            input_logic_code += f"        {function.name}(state_manager, event)\n"
            input_logic_code += "\n"

        logic_code = ""
        for function in self.logics:
            logic_code += f"        # {function.description}\n"
            logic_code += f"        {function.name}(state_manager)\n"
            logic_code += "\n"

        render_code = ""
        for function in self.renders:
            render_code += f"        # {function.description}\n"
            render_code += f"        {function.name}(state_manager)\n"
            render_code += "\n"
        # add all logics code
        all_code += APPEND_CODE.format(
            input_logic_code=input_logic_code,
            logic_code=logic_code,
            render_code=render_code,
        )
        return all_code
