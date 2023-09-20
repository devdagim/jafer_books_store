import importlib


class Execute:
    """
    Execute used to dynamically execute controllers and other classes.

    Attributes:
        executable_module_path (str): The path to the module containing the
            controller/executable class.
        executable_module_name (str): The name of the controller/executable
            class and method in the format 'ClassName@method_name'.
        **kwargs: Additional keyword arguments to be passed to the executed
            method.
    """

    def __init__(
        self,
        executable_module_path: str,
        executable_module_name: str,
        *args,
        **kwargs
    ):
        """
        Initialize the Execute instance.

        Args:
            executable_module_path (str): The path to the module containing
                the controller class.
            executable_module_name (str): The name of the controller class and
                method in the format 'ClassName@method_name'.
            **kwargs: Additional keyword arguments to be passed to the executed
                method.
        """
        self.executable_module_path = executable_module_path
        self.executable_module_name = executable_module_name
        self.args = args
        self.kwargs = kwargs

    def exc(self):
        """
        Execute the specified controller and method.

        Returns:
            The result of the executed method.

        Raises:
            ImportError: If the module cannot be imported.
            AttributeError: If the controller class or method cannot be found.
        """
        # splitting the class and the method
        executable_module_name_parts = self.executable_module_name.split("@")
        class_name = executable_module_name_parts[0]
        method_name = executable_module_name_parts[1]

        try:
            module = importlib.import_module(
                "telegram_bot." + self.executable_module_path
            )
            controller_class = getattr(module, class_name)
            func = getattr(controller_class, method_name)
            return func(self=controller_class(), *self.args, **self.kwargs)

        except (ImportError, AttributeError):
            raise "Controller or function not found."
