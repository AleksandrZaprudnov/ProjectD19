import datetime
from datetime import datetime as d_t


# range_day = {
#     1: (datetime.time(0, 0, 0), datetime.time(8, 0, 0)),
#     2: (datetime.time(8, 0, 0), datetime.time(14, 0, 0)),
#     3: (datetime.time(14, 0, 0), datetime.time(20, 0, 0)),
# }
#
# time_now = datetime.datetime.now().time()
#
# for range_cur in range_day:
#     print(f'Текущий диапазон: {range_day[range_cur][0]}')
#     if range_day[range_cur][0] <= time_now < range_day[range_cur][1]:
#         start = d_t.combine(datetime.datetime.today(), range_day[range_cur][0])
#         end = d_t.combine(datetime.datetime.today(), range_day[range_cur][1])
#         break
#
# print(f'Диапазон: {start} - {end}')
