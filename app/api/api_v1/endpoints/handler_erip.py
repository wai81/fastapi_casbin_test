from typing import TypeVar, Generic, Type, Dict, Any
import xml.etree.ElementTree as XmlET
import simplexml
from fastapi import APIRouter, Request, Response, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.depend import get_db

T = TypeVar("T", bound=BaseModel)


class XmlData(BaseModel):
    word: str


class XmlBody(Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    async def __call__(self, request: Request) -> T:
        body = await request.body()
        dict_data = simplexml.loads(body)
        print(dict_data)
        return self.model_class.parse_obj(dict_data["Request"])


router = APIRouter()


@router.post("/")
async def erip_request(request: Request, db: Session = Depends(get_db)):
    # async def submit(request: XmlData = Depends(XmlBody(XmlData))):
    content_type = request.headers['content-type']  # request.headers.get("content-type", None)
    print(content_type)
    body = await request.body()
    if len(body):
        dict_data = simplexml.loads(body)
        response = await handler_request(request=dict_data)
        print(f'response => {response}')
        # return Response(content=body, media_type="multipart/form-data; charset=windows-1251")
        return Response(content=response, media_type="application/xml")
    else:
        raise HTTPException(status_code=400, detail=f'Request empty')

    # if content_type == 'multipart/form-data; charset=windows-1251':
    #
    #
    #     if len(body):
    #         return Response(content=body, media_type="application/xml")
    #     else:
    #         raise HTTPException(status_code=400, detail=f'Content type {content_type} not supported')
    # else:
    #     raise HTTPException(status_code=400, detail=f'Content type {content_type} not supported')


def handler_service_info(request: Dict[str, Any]):
    p_debit = 12.50
    penalty = 0
    service_no = request['ServiceProvider_Request']['ServiceNo']
    personal_account = request['ServiceProvider_Request']['PersonalAccount']
    request_id = request['ServiceProvider_Request']['RequestId']
    # 'Amount Editable="N" MinAmount="0,01" MaxAmount="1000,00"': {

    service_info = {
        'Amount': {
            'Debt': p_debit,
            # 'Penalty': ''
        },
        'Name': {
            'Surname': "Иванов",
            'FirstName': "Иван",
            'Patronymic': "Иванович"
        },
        'Address': {
            'City': "Минск",
            'Street': "Пушкинa",
            'House': "10",
            'Building': "l",
            'Apartment': "100"
        },
        'Info': {
            'InfoLine': f'Стоимость услуги:{p_debit}'
        }

    }
    response = {
        'ServiceProvider_Request': {
            'ServiceInfo': service_info,
            'NextRequestType': "TransactionStart"
        }
    }
    xml_response=simplexml.dumps(response)
    res = xml_response.encode('cp1251')
    return res
    # return simplexml.dumps(response)


async def handler_request(request: Dict[str, Any]):
    request_version = request['ServiceProvider_Request']['Version']
    request_type = request['ServiceProvider_Request']['RequestType']
    if request_type == 'ServiceInfo':
        service_number = request['ServiceProvider_Request']['ServiceNo']
        personal_account = request['ServiceProvider_Request']['PersonalAccount']
        request_id = request['ServiceProvider_Request']['RequestId']
        if service_number is not None:  # определяем номер услуги
            # todo получаем номер услуги из базы
            pass
        else:
            raise HTTPException(status_code=400, detail=f'Ошибка выполнения платежа. Повторите платеж')

        response = handler_service_info(request)
    elif request_type == 'TransactionStart':
        pass
    elif request_type == 'TransactionResult':
        pass
    elif request_type == 'StornStart':
        pass
    elif request_type == 'StornResult':
        pass
    else:
        raise HTTPException(status_code=400, detail=f'Ошибка выполнения платежа. Повторите платеж')

    return response
