from .CleaningText import CleaningText
from .Classification import KNNClassification
from .Extract import ExtractPdf
from .Scores import TranskipScores, AchievementTranskip, DocumentScores
from .Support import ArraySupport
from .Summerize import Summerize

lib = [
    "CleaningText",
    "KNNClassification",
    "ExtractPdf",
    "TranskipScores",
    "DocumentScores",
    "ArraySupport",
    "AchievementTranskip",
    "Summerize"
]
__all__ = lib