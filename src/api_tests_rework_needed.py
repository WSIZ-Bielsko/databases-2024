import requests

from src.model import PlanItem

HOST = 'http://localhost:5000'


def create_plan_item():
    item = PlanItem(id=None, group_id=1, lecture_id=1, teacher_id=2,
                    room='S13', hour='16:15', day_of_week='Sat')
    dd = item.dict()
    print(dd)
    res = requests.post(f'{HOST}/plan-item', json=item.dict())
    pi = PlanItem(**(res.json()))
    print(pi)


def update_plan_item():
    item = PlanItem(id=1, group_id=5, lecture_id=5, teacher_id=5, room='S13',
                    hour='16:15', day_of_week='Sat')
    dd = item.dict()
    print(dd)
    res = requests.put(f'{HOST}/plan-item', json=item.dict())
    pi = PlanItem(**(res.json()))
    print('updated:', pi)


if __name__ == '__main__':
    # create_plan_item()
    update_plan_item()
