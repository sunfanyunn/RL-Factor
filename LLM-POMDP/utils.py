import ast
import importlib.util
import os
import random
import re
import string
import subprocess
import tempfile


def extract_variables_with_regex(code, keyword="state_manager"):
    """
    Extracts all variables used in the format `state_manager.variable_name` from the given code using regex.
    """
    pattern = rf"{keyword}\.(\w+)"
    matches = re.findall(pattern, code)
    return list(set(matches))  # Removing duplicates


def extract_error_location(code, traceback_str):
    error_line = None
    error_column = None

    # Extract error line and column from traceback
    traceback_lines = traceback_str.splitlines()
    for index, line in enumerate(traceback_lines):
        if "File " in line:
            file_match = re.search(r'File "([^"]+)", line (\d+), in ([^"]+)', line)
            if file_match:
                if file_match.group(1).endswith("initial.py"):
                    error_file, error_line, name = (
                        file_match.group(1),
                        int(file_match.group(2)),
                        file_match.group(3),
                    )

                    # Check if there are at least two lines below the current line
                    if index + 2 < len(traceback_lines):

                        error = traceback_lines[index + 2]

    parsed_code = parse_python_code_to_tree(code)
    if error_line is not None:
        return find_node_and_parents_at_line(parsed_code, error_line, name), error


def run_code(code):
    code = "import os\n" + 'os.environ["SDL_VIDEODRIVER"] = "dummy"\n' + code
    # Create a temporary Python file to store the code
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as tmp_file:
        tmp_file_name = tmp_file.name
        tmp_file.write(code)

    # Run the Python script using subprocess
    result = subprocess.run(["python", tmp_file_name], capture_output=True, text=True)

    # Capture stdout and stderr
    stdout = result.stdout
    stderr = result.stderr

    return stdout, stderr


def code_compilable(code):
    try:
        compile(code, "<string>", "exec")
        return True
    except Exception as e:
        print("cannot be compiled", e)
        return False


def extract_function_name_and_args(func_str):
    pattern = r"def\s+(\w+)\s*\((.*?)\):"
    match = re.search(pattern, func_str)
    if match:
        function_name = match.group(1)
        args = match.group(2).split(",")
        return function_name, args
    else:
        return None, None


def extract_variables(code):
    class VariableVisitor(ast.NodeVisitor):
        def __init__(self):
            self.variables = []

        def visit_Name(self, node):
            # Include only variables (excluding 'self' and not built-in functions)
            if isinstance(node.ctx, ast.Load) and node.id != "self":
                self.variables.append(node.id)

    # Parse the code to an AST
    tree = ast.parse(code)
    visitor = VariableVisitor()
    visitor.visit(tree)

    # Filter out duplicates and sort variables by length in descending order to avoid partial replacement issues
    unique_variables = sorted(set(visitor.variables), key=len, reverse=True)
    list_to_not_include = [
        "int",
        "float",
        "str",
        "bool",
        "tuple",
        "list",
        "dict",
        "np",
        "array",
    ]
    return [var for var in unique_variables if var not in list_to_not_include]


def check_function_for_state_change(function_string):
    """
    Parses a given Python function in string format to determine if any
    attributes of a 'state_manager' object are being modified.
    """
    # Parse the function string into an AST (Abstract Syntax Tree)
    try:
        tree = ast.parse(function_string)
    except SyntaxError:
        return "The function string contains syntax errors."

    # Define a visitor class to inspect assignments
    class StateManagerAssignVisitor(ast.NodeVisitor):
        def __init__(self):
            self.modifies_state_manager = False

        def visit_Assign(self, node):
            # Check if the left side of the assignment is an attribute of state_manager
            for target in node.targets:
                if isinstance(target, ast.Attribute) and isinstance(
                    target.value, ast.Name
                ):
                    if target.value.id == "state_manager":
                        self.modifies_state_manager = True

        def visit_AugAssign(self, node):
            # Check if the target of the augmented assignment is an attribute of state_manager
            if isinstance(node.target, ast.Attribute) and isinstance(
                node.target.value, ast.Name
            ):
                if node.target.value.id == "state_manager":
                    self.modifies_state_manager = True

    # Create an instance of the visitor and walk the AST
    visitor = StateManagerAssignVisitor()
    visitor.visit(tree)

    # Return the result
    return visitor.modifies_state_manager


def find_node_and_parents_at_line(node, line, name, parents=None):
    if parents is None:
        parents = []
    if node.node_type == "root":
        pass
    # if hasattr(node, "lineno") and node.lineno == line:
    if hasattr(node, "name") and node.name == name:

        # if hasattr(node, "lineno") and node.lineno == line:
        return [i.name for i in parents[1:]] + [node.name]

    for child in node.children:

        result = find_node_and_parents_at_line(child, line, name, parents + [node])
        if result:
            return result

    return None


def import_backbone(game_path):
    # dynamically import the 'prompt' from prompt.py under game_path
    prompt_path = os.path.join(game_path, "prompt.py")
    spec = importlib.util.spec_from_file_location("prompt_module", prompt_path)
    prompt_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prompt_module)
    prompt = (
        prompt_module.complete_code_prompt
    )  # dynamically import the 'prompt' variable
    codebase = (
        prompt_module.complete_backbone_code
    )  # dynamically import the 'prompt' variable
    return prompt, codebase


def generate_random_string(length=10):
    """Generate a random string of given length with only alphabetical characters."""
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def extract_markdown_content(s, language="javascript"):
    pattern = r"```{}\s*([\s\S]*?)\s*```".format(language)
    matches = re.findall(pattern, s)
    return "\n".join(matches)


def extract_function_name(func_str):
    pattern = r"def\s+(\w+)\s*\((.*?)\):"
    match = re.search(pattern, func_str)
    if match:
        return match.group(1)
    else:
        return None


def extract_class_name(class_str):
    pattern = r"class\s+(\w+)\s*(\(.*\))?:"
    match = re.search(pattern, class_str)
    if match:
        return match.group(1)
    else:
        return None


def extract_script_name(s):
    pattern = r"var (\w+) = pc\.createScript\(['\"](\w+)['\"]\)"
    match = re.search(pattern, s)

    if match:
        variable_name = match.group(1)
        script_name = match.group(2)
    else:
        return None, None
    return variable_name, script_name


def replace_variable_name(code, old_name, new_name):
    # This regex matches the old_name only if it's surrounded by non-word characters or at the start/end of the string
    pattern = r"(?<!\w){}(?!\w)".format(re.escape(old_name))
    return re.sub(pattern, new_name, code)


def generate_backbone_code(game_graph, user_prompt, llm):
    # initialize each component

    # Placeholder component prompt
    backbone_prompt = PromptTemplate(
        input_variables=[
            "user_prompt",
            "game_graph",
        ],
        template=implement_backbone_prompt,
    )
    backbone_prompt = implement_backbone_prompt.format(
        user_prompt=user_prompt,
        game_graph=game_graph,
    )

    generated_code = llm(backbone_prompt)
    code = extract_markdown_content(generated_code, "python")
    return code


class StateManagerVariableExtractor(ast.NodeVisitor):
    def __init__(self):
        self.accessed_variables = set()
        self.modified_variables = set()

    def visit_Attribute(self, node):
        # Check if the attribute is of 'state_manager'
        if isinstance(node.value, ast.Name) and node.value.id == "state_manager":
            self.accessed_variables.add(node.attr)
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Handles standard assignments
        self._handle_possible_modification(node.targets)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        # Handles augmented assignments
        self._handle_possible_modification([node.target])
        self.generic_visit(node)

    def _handle_possible_modification(self, targets):
        # Handle possible modifications in targets
        for target in targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "state_manager"
            ):
                self.modified_variables.add(target.attr)

    def visit_For(self, node):
        # Handle potential modifications in for-loop
        self._handle_possible_modification([node.target])
        self.generic_visit(node)

    def visit_While(self, node):
        # Handle potential modifications in while-loop
        # Note: This is a simplification, as while-loops don't necessarily
        # modify variables in their test condition.
        self.generic_visit(node)

    def visit_With(self, node):
        # Handle potential modifications in with-statement
        # Note: This is a simplification, as with-statements don't necessarily
        # modify variables.
        self.generic_visit(node)


def extract_modified_state_manager_variables(func_str):
    tree = ast.parse(func_str)
    extractor = StateManagerVariableExtractor()
    extractor.visit(tree)
    return extractor.accessed_variables, extractor.modified_variables


if __name__ == "__main__":
    # Example usage
    assignment_str = "self.state = int(10), x, y, tuple((0,0,0)), np.array([1,2,3])"
    variables = extract_variables(assignment_str)
    print(variables)
    input()
    # Example usage
    func_str = """
def update_bird_position(state_manager):
    gravity = 1
    flap_power = 15
    movement_flag = 'down' if state_manager.bird_velocity_y > 0 else 'up'
    max_descend_speed = 10
    if movement_flag == 'up':
        state_manager.bird_velocity_y = max(-flap_power, state_manager.bird_velocity_y - gravity)
    else:
        state_manager.bird_velocity_y = min(max_descend_speed, state_manager.bird_velocity_y + gravity)
    state_manager.bird_position_y += state_manager.bird_velocity_y
    state_manager.bird_position_y = max(0, min(state_manager.bird_position_y, state_manager.screen_height - state_manager.bird_height))
"""

    accessed, modified = extract_modified_state_manager_variables(func_str)
    print("Accessed Variables:", accessed)
    print("Modified Variables:", modified)
    input()

    s = """def draw_bird(state_manager):
    bird_rect = pygame.Rect(state_manager.bird_x, state_manager.bird_y, state_manager.bird_width, state_manager.bird_height)
    pygame.draw.rect(state_manager.screen, (255, 200, 0), bird_rect)"""
    print(extract_variables_with_regex(s, "state_manager"))

    s = "var Score = pc.createScript('score')"
    print(extract_script_name(s))
    # Example:
    code = """
    var x = 10;
    if (x == localVar) {
        anotherVar = x;
    }
    """

    new_code = replace_variable_name(code, "x", "myVar")
    print(new_code)
