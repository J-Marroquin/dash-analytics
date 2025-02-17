import os
import importlib
import inspect
from DashboardAgrotechApp.logger import Logger

class GraphManager:
    def __init__(self):
        """
        Initializes the GraphManager with an empty dictionary of graphs and a logger.
        
        The `graphs` dictionary will store graph names and their corresponding functions.
        The `logger` is used to log errors if an invalid graph name is provided.
        """ 
        self.logger = Logger()   
        self.graphs = {}
        file_path = os.path.dirname(os.path.abspath(__file__))
        graphs_folder = os.path.join(file_path, "graphs")
        self._register_graphs(graphs_folder)
        
    
    def _register_graphs(self, graphs_folder):
        """
        Scans the specified directory for Python files and registers graph functions.
        
        Args:
        -----
        param graphs_folder (str):
            The folder containing Python files with graph functions.
        """
        for filename in os.listdir(graphs_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove .py extension
                try:
                    module = importlib.import_module(f"DashboardAgrotechApp.graphs.{module_name}")
                    for name, func in inspect.getmembers(module, inspect.isfunction):
                        if self._is_valid_graph_function(func):
                            graph_name = f"{name}"
                            self.graphs[graph_name] = func
                            self.logger.log_info(f"Registered graph: {graph_name}")
                except Exception as e:
                    self.logger.log_error(f"Error importing module {module_name}: {e}")
    
    def _is_valid_graph_function(self, func)->bool:
        """
        Validates if the given function is a valid graph plotting function.

        A valid graph function is defined as having a `__name__` attribute and a name that starts with "plot_".

        Args:
        -----
            func (callable): The function to validate.

        Returns:
        --------
            bool: True if the function is valid, False otherwise.
        """
        return hasattr(func, "__name__") and func.__name__.startswith("plot_")
    
    def get_func(self, function_name:str):
        """
        Retrieves the graph-generating function based on the provided name.

        If the graph is registered, it returns the corresponding function.
        If the graph is not registered, it logs an error and raises a `ValueError`.

        Args:
        -----
        function_name (str): 
            The name of the graph to retrieve.

        Returns:
        --------
        callable
            The function corresponding to the specified graph name. This function should
            return a Plotly figure object when called with the appropriate data.
        
        Raises:
        -------
        ValueError
            If the graph name is not found in the `graphs` dictionary.
        
        Example:
        --------
        >>> plot_func = graph_manager.func("egg_registration")
        >>> fig = plot_func(data)
        >>> fig.show()
        """
        if function_name in self.graphs:
            return self.graphs[function_name]
        else:
            self.logger.log_error(f"Graph type '{function_name}' is not registered.")
            raise ValueError(f"Graph type '{function_name}' is not registered.")

    