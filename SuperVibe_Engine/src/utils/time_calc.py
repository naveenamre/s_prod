# src/utils/time_calc.py

def mins_to_ms(minutes: int) -> int:
    """Minutes ko Milliseconds mein convert karta hai (Super Productivity Format)"""
    return int(minutes * 60 * 1000)

def hours_to_ms(hours: float) -> int:
    """Hours ko Milliseconds mein convert karta hai"""
    return int(hours * 60 * 60 * 1000)

def ms_to_mins(ms: int) -> int:
    """Milliseconds ko wapas Minutes mein convert karta hai"""
    return int(ms / (60 * 1000))

def get_pomodoro_split(duration_mins: int, work_mins: int = 50, break_mins: int = 10) -> dict:
    """
    🍅 Advanced: Agar task lamba hai, toh usko Pomodoro slots mein todne ka jugad.
    (Future upgrade ke liye)
    """
    cycles = duration_mins // (work_mins + break_mins)
    remainder = duration_mins % (work_mins + break_mins)
    
    return {
        "total_ms": mins_to_ms(duration_mins),
        "work_ms": mins_to_ms(work_mins),
        "break_ms": mins_to_ms(break_mins),
        "cycles": cycles,
        "remainder_ms": mins_to_ms(remainder)
    }