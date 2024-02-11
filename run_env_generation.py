import pickle
import importlib
import json
import argparse
import os
import sys
from game_structure import GameRep
from openai import OpenAI


def modify_python_code_for_pygbag(input_code):
    # Step 3: Replace "def main():" with "async def main():"
    modified_code = input_code.replace("def main():", "async def main():")

    # Step 1: Replace "main()" with "asyncio.run(main())"
    modified_code = modified_code.replace(
        'if __name__ == "__main__":\n    main()',
        'if __name__ == "__main__":\n    asyncio.run(main())',
    )

    # Step 2: Add "await asyncio.sleep(0)" after "clock.tick(state_manager.fps)"
    if "clock.tick(state_manager.fps)" in modified_code:
        modified_code = modified_code.replace(
            "clock.tick(state_manager.fps)",
            "clock.tick(state_manager.fps)\n        await asyncio.sleep(0)",
        )

    return "import asyncio\n" + modified_code


def for_pygbag(game):
    code = game.export_code()
    modified_code = modify_python_code_for_pygbag(code)
    with open("pygbag_game/main.py", "w") as f:
        f.write(modified_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game Parameters')
    parser.add_argument('--log_dir', type=str, help='Directory for logs')
    parser.add_argument('--env_name', type=str, help='Environment name')
    parser.add_argument('--game_template', type=str, help='Game template')
    parser.add_argument('--debug_mode', type=int, choices=[1, 2, 3], help='Debug mode')

    # Parse arguments
    args = parser.parse_args()

    # Use arguments
    log_dir = args.log_dir
    game_template = args.game_template
    debug_mode = args.mode

    # Set these game constants
    WIDTH, HEIGHT, FPS = 800, 600, 60
    log_dir = sys.argv[1]
    game_template = sys.argv[2]

    #api_key_path = '/ccn2/u/locross/llmv_marl/llm_plan/lc_api_key.json'
    api_key_path = '/Users/locro/Documents/Stanford/lc_api_key.json'
    OPENAI_KEYS = json.load(open(api_key_path, 'r'))
    api_key = OPENAI_KEYS['API_KEY']
    client = OpenAI(api_key=api_key)

    game = GameRep(
        HEIGHT, WIDTH, FPS, log_dir=log_dir, debug_mode=debug_mode, client=client
    )
    pass_test, error_msg = game.pass_sanity_check()
    print(error_msg)
    assert pass_test

    if debug_mode == 1:
        # Function to import 'prompts.py' dynamically from a given directory
        module_path = f"games.single_player_games.{game_template}.prompts"
        module = importlib.import_module(module_path)
        iterative_prompts = module.iterative_prompts.split("\n")
        for query_idx, query in enumerate(iterative_prompts):
            if len(query):
                for response in game.process_user_query(query.strip()):
                    print(response)

                # save game repr
                game.client = None
                filename = f"{game.log_dir}/{game.query_idx-1}/{game.num_api_calls}_game_rep.pkl"
                with open(filename, "wb") as file:
                    pickle.dump(game, file)
                with open(f"{game.log_dir}/final.pkl", "wb") as file:
                    pickle.dump(game, file)

                game.client = client

                for_pygbag(game)
        code = game.export_code()
        implementation_path = os.path.join("env_design/envs/", args.env_name + ".py")
        with open(implementation_path, "w") as f:
            f.write(code)

    if debug_mode == 2:
        # debug from scratch
        while True:
            query = input("Enter a query:")
            for response in game.process_user_query(query):
                print(response)
            # save game repr
            game.client = None
            filename = (
                f"{game.log_dir}/{game.query_idx-1}/{game.num_api_calls}_game_rep.pkl"
            )
            with open(filename, "wb") as file:
                pickle.dump(game, file)
            game.client = client

            for_pygbag(game)
        code = game.export_code()
        implementation_path = os.path.join("env_design/envs/", args.env_name + ".py")
        with open(implementation_path, "w") as f:
            f.write(code)

    if debug_mode == 3:
        # load game rep from a file and evaluate
        filename = sys.argv[2]
        game = pickle.load(open(filename, "rb"))
        game.client = client
        code = game.export_code()
        implementation_path = "env_design/envs/flappy_bird_test.py"
        with open(implementation_path, "w") as f:
            f.write(code)
