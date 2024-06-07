from .CleaningText import CleaningText
from .Classification import KNNClassification
from .Extract import ExtractPdf
from .Scores import TranskipScores, AchievementTranskip
from .Support import ArraySupport

lib = [
    "CleaningText",
    "KNNClassification",
    "ExtractPdf",
    "TranskipScores",
    "ArraySupport",
    "AchievementTranskip"
]
__all__ = lib