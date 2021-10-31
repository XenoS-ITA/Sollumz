import traceback
import time
from abc import abstractmethod
from Sollumz.sollumz_properties import DrawableType


class SOLLUMZ_OT_base():
    bl_options = {"UNDO"}
    bl_action = "do"
    bl_showtime = False

    def __init__(self):
        self.messages = []

    @abstractmethod
    def run(self, context):
        pass

    def execute(self, context):
        start = time.time()
        try:
            result = self.run(context)
        except:
            result = False
            self.error(
                f"Error occured running operator : {self.bl_idname} \n {traceback.format_exc()}")
        end = time.time()

        if self.bl_showtime and result == True:
            self.message(
                f"{self.bl_label} took {round(end - start, 3)} seconds to {self.bl_action}.")

        if len(self.messages) > 0:
            self.message('\n'.join(self.messages))

        if result:
            return {"FINISHED"}
        else:
            return {"CANCELLED"}

    def message(self, msg):
        self.report({"INFO"}, msg)

    def warning(self, msg):
        self.report({"WARNING"}, msg)

    def error(self, msg):
        self.report({"ERROR"}, msg)

    def success(self, msg=None, show_msg=True, show_completed=True):
        if show_msg:
            self.message(
                f"{self.bl_action}{f' {msg} ' if msg else ' '}{'completed.' if show_completed else ''}")
        return True

    def fail(self, traceback):
        self.error(f"Failure to {self.bl_action} because: \n {traceback}")
        return False

    def is_sollum_object_in_objects(self, objs):
        for obj in objs:
            if obj.sollum_type != DrawableType.NONE:
                return True
        return False

    def is_sollum_type(self, obj, type):
        return obj.sollum_type in type._value2member_map_

    def obj_is_sollumtype(self, obj, sollum_type):
        if not (obj and obj.sollum_type == sollum_type):
            return False
        return True
