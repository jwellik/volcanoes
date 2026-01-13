"""
EruptionSet class for collections of eruptions.
"""
from typing import List, Optional, Union, Iterator
from .eruption import Eruption


class EruptionSet:
    """A collection of eruptions with filtering and analysis methods."""

    def __init__(self, eruptions: List[Eruption]):
        """Initialize with a list of Eruption objects."""
        self._eruptions = eruptions

    def __len__(self) -> int:
        """Return the number of eruptions in the set."""
        return len(self._eruptions)

    def __getitem__(self, index: Union[int, slice]) -> Union[Eruption, 'EruptionSet']:
        """Get eruption(s) by index."""
        if isinstance(index, slice):
            return EruptionSet(self._eruptions[index])
        return self._eruptions[index]

    def __iter__(self) -> Iterator[Eruption]:
        """Iterate over eruptions."""
        return iter(self._eruptions)

    @property
    def eruptions(self) -> List[Eruption]:
        """Get the list of eruptions."""
        return self._eruptions

    def filter_by_volcano_number(self, volcano_number: int) -> 'EruptionSet':
        """Filter eruptions by volcano number."""
        filtered = [e for e in self._eruptions if e.volcano_number == volcano_number]
        return EruptionSet(filtered)

    def get_volcano_numbers(self) -> List[int]:
        """Get a list of unique volcano numbers."""
        numbers = [e.volcano_number for e in self._eruptions if e.volcano_number is not None]
        return sorted(list(set(numbers)))

    def print(self, limit: Optional[int] = None):
        """Print information about eruptions in the set."""
        eruptions_to_print = self._eruptions[:limit] if limit else self._eruptions

        print(f"EruptionSet with {len(self._eruptions)} eruptions:")
        print("-" * 80)

        for i, eruption in enumerate(eruptions_to_print):
            volcano_num = eruption.volcano_number if eruption.volcano_number else "Unknown"
            print(f"{i + 1:3d}. Volcano #{volcano_num}")

        if limit and len(self._eruptions) > limit:
            print(f"... and {len(self._eruptions) - limit} more")

    def summary_stats(self) -> dict:
        """Get summary statistics for the eruption set."""
        volcano_numbers = [e.volcano_number for e in self._eruptions if e.volcano_number is not None]

        return {
            'total_eruptions': len(self._eruptions),
            'unique_volcanoes': len(set(volcano_numbers)),
        }
