import inspect
import common.frames as cf
from common.frames import FrameDisplayFilledRectangle

classes = inspect.getmembers(cf, lambda member: inspect.isclass(member) and member.__module__ == 'common.frames')

#print(classes)

print(FrameDisplayFilledRectangle().comment)

#for i in classes:
#    print(i[1])
#    comment = i[1]().get_comment()
#    if comment:
#        print(comment)