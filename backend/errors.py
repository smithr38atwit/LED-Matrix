class DisplayManagerError(Exception):
    """Base error for display lifecycle operations."""


class DisplayNotFoundError(DisplayManagerError):
    def __init__(self, display_id: str):
        super().__init__(f"Unknown display id: {display_id}")
        self.display_id = display_id


class DisplayNotControllableError(DisplayManagerError):
    def __init__(self, display_id: str):
        super().__init__(f"Display is registered but not controllable: {display_id}")
        self.display_id = display_id
