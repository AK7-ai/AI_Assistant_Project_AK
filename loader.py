"""
loader.py

Utilities for loading PMData files.

This module centralizes all file loading operations so that the rest of the project does not need to know where the data is stored.
"""

from pathlib import Path
import pandas as pd


class PMDataLoader:
    """
    Loader class for the PMData dataset.

    Parameters
    ----------
    data_dir : str | Path
        Path to the PMData directory.
    """

    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)

    def _participant_path(self, participant_id: str) -> Path:
        """
        Returns the directory corresponding to one participant.

        Example:
            PMData/p01
        """
        return self.data_dir / participant_id

    def _load_json(self, filepath: Path) -> pd.DataFrame:
        """
        Generic JSON loader.

        Automatically converts known datetime columns.
        """

        df = pd.read_json(filepath)

        datetime_columns = [
            "dateTime",
            "startTime",
            "originalStartTime",
            "lastModified",
            "dateOfSleep",
            "endTime",
            "createdAt",
            "updatedAt",
            "effective_time_frame",
            "end_date_time",
        ]

        for column in datetime_columns:
            if column in df.columns:
                df[column] = pd.to_datetime(
                    df[column],
                    format="mixed",
                    errors="coerce"
                )
        return df

    def _load_csv(self, filepath: Path) -> pd.DataFrame:
        """
        Generic CSV loader.
        """
        return pd.read_csv(filepath)


    def load_steps(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "steps.json"
        )

    def load_sleep(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "sleep.json"
        )

    def load_sleep_score(self, participant_id):
        return self._load_csv(
            self._participant_path(participant_id)
            / "fitbit"
            / "sleep_score.csv"
        )

    def load_heart_rate(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "heart_rate.json"
        )

    def load_resting_heart_rate(self, participant_id):
        """
        Load resting heart rate data.
        """

        df = self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "resting_heart_rate.json"
        )

        df["restingHeartRate"] = df["value"].apply(lambda x: x["value"])

        return df

    def load_calories(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "calories.json"
        )

    def load_distance(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "distance.json"
        )

    def load_exercise(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "exercise.json"
        )

    def load_sedentary_minutes(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "sedentary_minutes.json"
        )

    def load_lightly_active_minutes(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "lightly_active_minutes.json"
        )

    def load_moderately_active_minutes(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "moderately_active_minutes.json"
        )

    def load_very_active_minutes(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "very_active_minutes.json"
        )

    def load_heart_rate_zones(self, participant_id):
        return self._load_json(
            self._participant_path(participant_id)
            / "fitbit"
            / "time_in_heart_rate_zones.json"
        )


    def load_reporting(self, participant_id):
        return self._load_csv(
            self._participant_path(participant_id)
            / "googledocs"
            / "reporting.csv"
        )


    def load_wellness(self, participant_id):

        df = self._load_csv(
            self._participant_path(participant_id)
            / "pmsys"
            / "wellness.csv"
        )

        df["effective_time_frame"] = pd.to_datetime(
            df["effective_time_frame"],
            errors="coerce"
        )

        return df

    def load_injury(self, participant_id):

        df = self._load_csv(
            self._participant_path(participant_id)
            / "pmsys"
            / "injury.csv"
        )

        df["effective_time_frame"] = pd.to_datetime(
            df["effective_time_frame"],
            errors="coerce"
        )

        return df

    def load_srpe(self, participant_id):

        df = self._load_csv(
            self._participant_path(participant_id)
            / "pmsys"
            / "srpe.csv"
        )

        df["end_date_time"] = pd.to_datetime(
            df["end_date_time"],
            errors="coerce"
        )

        return df


    def list_participants(self):
        """
        Returns all available participant IDs.

        Example
        -------
        ['p01', 'p02', ..., 'p16']
        """
        return sorted(
            folder.name
            for folder in self.data_dir.iterdir()
            if folder.is_dir() and folder.name.startswith("p")
        )
