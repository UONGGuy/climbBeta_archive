# app/database/gym_builder.py

from app.models import *
from sqlalchemy.orm import Session

class GymBuilder:
    def __init__(self, gym_info: dict, session: Session):
        self.gym_info = gym_info
        self.session = session
        self.gym = None

    def build(self):
        """Main builder method to create gym and associations"""
        self._create_gym()
        self._assign_features()
        return self.gym

    def _create_gym(self):
        """Map basic gym fields + enums"""
        self.gym = ClimbingGym(
            name=self.gym_info.get("Name"),
            franchiser=self._resolve_enum(eFranchiser, "Franchiser"),
            status=self._resolve_enum(eGymStatus, "Status"),
            grading_system=self._resolve_enum(eGradingSystem, "Grading system"),
            mat_hire=self._resolve_enum(eMatHire, "Mat hire"),
            locker_type=self._resolve_enum(eLockerTypes, "Lockers"),
            notes=self.gym_info.get("Extra notes")
        )
        self.session.add(self.gym)

    def _assign_features(self):
        """Assign many-to-many relationships via association table"""
        features = []

        # Climbing Activities
        activities = self._get_dropdown_list("Climbing offered")
        for activity in activities:
            enum_val = self._resolve_enum(eClimbActivities, value=activity)
            features.append(ClimbingGymFeatures(activity=enum_val))

        # Climbing Boards
        boards = self._get_dropdown_list("Board climbing")
        for board in boards:
            enum_val = self._resolve_enum(eClimbBoard, value=board)
            self.gym.boards.append(ClimbingGymFeatures(board=enum_val))

        # Link all features to the gym
        self.gym.features = features

    def _resolve_enum(self, enum_cls, key=None, value=None):
        """Safe enum resolution with fallback"""
        try:
            val = value or self.gym_info.get(key)
            return enum_cls[val.upper().replace(" ", "_")]
        except Exception:
            return None

    def _get_dropdown_list(self, key: str):
        val = self.gym_info.get(key)
        return [v.strip() for v in val.split(",")] if val else []

