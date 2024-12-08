import sys
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
from typing import Optional

from utils import load_context, get_random_decision_quote
from workflow import State
from storage import create_decision_dir
from storage import create_decision_dir
import observe
import consult
import assemble

def display_welcome():
    """Display welcome message and random quote"""
    clear()
    print("Welcome to Consilio.\n")
    print(get_random_decision_quote())
    print("\nMay you make wise decisions.\n")

def run_repl(state: State):
    """Run the interactive REPL"""
    # Define valid commands and their completions
    commands = {
        'o': 'observe',
        'c': 'consult'
    }
    
    # Create completer with both short and full forms
    command_completer = WordCompleter(['observe', 'consult', 'o', 'c'], ignore_case=True)
    session = PromptSession(completer=command_completer)
    
    while True:
        try:
            command = session.prompt("\nEnter command (O/C) or Ctrl+C to exit: ").lower()
            
            # Normalize command - convert single letter to full command
            if command in commands:
                command = commands[command]
            
            if command in ['o', 'observe']:
                result = observe.observe(state.doc_path, state.context)
                print(observe.xml_to_markdown(result))
                
            elif command in ['c', 'consult']:
                # Step 1: Run assembly to get perspectives
                assembly_result = assemble.assemble(state.doc_path, state.context)
                print("\nHere are the perspectives identified:")
                print(assemble.xml_to_markdown(assembly_result))
                
                # Step 2: Ask for user confirmation
                proceed = session.prompt("\nReady to proceed with consultation? (Y/n): ")
                if proceed.lower() not in ['y', 'yes', '']:
                    continue
                
                # Step 3: Run consultation with assembled perspectives
                result = consult.consult(state.doc_path, assembly_result, state.context)
                print(result)  # This will show opinions from each perspective
                
            else:
                print("Invalid command. Please use 'O' or 'C' (or 'observe'/'consult')")
                
        except KeyboardInterrupt:
            print("\nExiting Consilio...")
            sys.exit(0)
        except Exception as e:
            print(f"\nError: {str(e)}")

def main(context_path: Optional[Path] = None, doc_path: Optional[Path] = None):
    """Main entry point for Consilio"""
    display_welcome()

    # Load context
    context = load_context(context_path)
    
    if not doc_path:
        doc_path = Path(input("Enter path to decision document: "))
    
    # Create decision directory
    decision_dir = create_decision_dir(doc_path.stem)
    
    # Initialize state
    state = State(
        decision_dir=decision_dir,
        context={"domain": context.domain, 
                "user_role": context.user_role,
                "perspective": context.perspective},
        stage="observe",
        doc_path=doc_path
    )
    
    # Start REPL
    run_repl(state)


if __name__ == "__main__":
    main()
