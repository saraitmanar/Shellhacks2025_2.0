# gradeBands.py
from abc import ABC, abstractmethod

class GradeBand(ABC):
    """Interface for a grade band. Each band returns a fact for a body part key."""
    @abstractmethod
    def fact(self, body_part: str) -> str | None:
        ...

class K5(GradeBand):
    _facts = {
        "heart": "Your heart beats faster when you run to push extra oxygen to your muscles—like stepping on the gas pedal!"

    }
    def fact(self, body_part: str) -> str | None:
        return self._facts.get(body_part)

class SixToEight(GradeBand):
    _facts = {
        "heart": "During exercise, your sympathetic nervous system increases heart rate and stroke volume so more oxygenated blood reaches working muscles."
    }
    def fact(self, body_part: str) -> str | None:
        return self._facts.get(body_part)

class NineToTwelve(GradeBand):
    _facts = {
        "heart": "Heart rate rises with metabolic demand: β-adrenergic stimulation increases SA-node firing; venous return and Frank-Starling increase stroke volume, boosting cardiac output (CO = HR × SV)."
    }
    def fact(self, body_part: str) -> str | None:
        return self._facts.get(body_part)

# Optional: a registry to make lookup simple in app.py
BANDS = {
    "K-5": K5(),
    "6-8": SixToEight(),
    "9-12": NineToTwelve(),
}
