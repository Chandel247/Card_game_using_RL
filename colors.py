class Colors:
    """ANSI color codes for terminal output"""
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    @staticmethod
    def color_text(text: str, color: str, bold: bool = False) -> str:
        """Return colored text"""
        style = Colors.BOLD if bold else ''
        return f"{style}{color}{text}{Colors.RESET}"
    
    @staticmethod
    def hp_color(hp: int, max_hp: int) -> str:
        """Return color based on HP percentage"""
        percentage = hp / max_hp
        if percentage > 0.6:
            return Colors.GREEN
        elif percentage > 0.3:
            return Colors.YELLOW
        else:
            return Colors.RED
    
    @staticmethod
    def player_color(text: str) -> str:
        """Color for player text"""
        return Colors.color_text(text, Colors.CYAN, bold=True)
    
    @staticmethod
    def opponent_color(text: str) -> str:
        """Color for opponent text"""
        return Colors.color_text(text, Colors.RED, bold=True)
    
    @staticmethod
    def effect_color(text: str) -> str:
        """Color for effect text"""
        return Colors.color_text(text, Colors.MAGENTA)
    
    @staticmethod
    def success_color(text: str) -> str:
        """Color for success messages"""
        return Colors.color_text(text, Colors.GREEN, bold=True)
    
    @staticmethod
    def warning_color(text: str) -> str:
        """Color for warnings"""
        return Colors.color_text(text, Colors.YELLOW, bold=True)
    
    @staticmethod
    def error_color(text: str) -> str:
        """Color for errors"""
        return Colors.color_text(text, Colors.RED, bold=True)
    
    @staticmethod
    def header_color(text: str) -> str:
        """Color for headers"""
        return Colors.color_text(text, Colors.BRIGHT_CYAN, bold=True)
