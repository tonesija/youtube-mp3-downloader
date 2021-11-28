class ProgressListener:
    """Abstract progress listener."""

    def on_progress_change(self, name, value):
        """Fire method.

        Args:
            name (str): label of the progress.
            value (numeric): progresses value.
        """

        pass


class RealVideoNameFoundListener:

    def on_real_video_name_found(self, user_typed_name, real_video_name):
        pass
