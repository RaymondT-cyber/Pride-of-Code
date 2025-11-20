"""Code Executor - Safe Python execution with band API integration.

This module provides a sandboxed environment for running student code
with access to the Band API.
"""

import sys
import io
import traceback
from typing import Tuple, Dict, Any
from gameplay.band_api import BandAPI


class CodeExecutor:
    """Executes student Python code in a controlled environment."""
    
    def __init__(self):
        self.band_api = BandAPI()
        self.output_buffer = []
        self.error_message = None
        
    def reset(self):
        """Reset the execution environment."""
        self.band_api.reset()
        self.output_buffer = []
        self.error_message = None
        
    def execute(self, code: str, initial_band_size: int = 16) -> Tuple[bool, str]:
        """Execute student code with the Band API.
        
        Args:
            code: Python code to execute
            initial_band_size: Number of band members to create
            
        Returns:
            (success: bool, output: str) tuple
        """
        self.reset()
        self.band_api.create_band(initial_band_size)
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            # Create safe global namespace with Band API
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'int': int,
                    'float': float,
                    'str': str,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    'True': True,
                    'False': False,
                    'None': None,
                    'abs': abs,
                    'min': min,
                    'max': max,
                    'sum': sum,
                    'round': round,
                },
                'band': self.band_api,
                'members': self.band_api.members,
                'brass': self.band_api.get_section('brass'),
                'woodwind': self.band_api.get_section('woodwind'),
                'percussion': self.band_api.get_section('percussion'),
                'guard': self.band_api.get_section('guard'),
            }
            
            # Execute the code
            exec(code, safe_globals)
            
            # Get output
            output = sys.stdout.getvalue()
            self.output_buffer.append(output)
            
            return True, output
            
        except SyntaxError as e:
            error_msg = f"Syntax Error on line {e.lineno}: {e.msg}"
            self.error_message = error_msg
            return False, error_msg
            
        except NameError as e:
            error_msg = f"Name Error: {str(e)}\n\nDid you forget to define a variable?"
            self.error_message = error_msg
            return False, error_msg
            
        except TypeError as e:
            error_msg = f"Type Error: {str(e)}\n\nCheck your function arguments."
            self.error_message = error_msg
            return False, error_msg
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}\n\n{traceback.format_exc()}"
            self.error_message = error_msg
            return False, error_msg
            
        finally:
            sys.stdout = old_stdout
            
    def get_band_members(self):
        """Get current band member positions."""
        return self.band_api.members
        
    def get_output(self) -> str:
        """Get all captured output."""
        return ''.join(self.output_buffer)
        
    def get_error(self) -> str:
        """Get error message if any."""
        return self.error_message or ''