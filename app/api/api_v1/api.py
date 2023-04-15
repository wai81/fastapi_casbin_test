from fastapi import APIRouter

from app.api.api_v1.endpoints import (receipt, organization, auth, handler_erip, handler_1c_enterprise,
                                      pay_terminal, order, user, subunit, booking_transport, transport)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth",
                          tags=["Auth (Авторизация)"])
api_router.include_router(user.router, prefix="/users",
                          tags=["Users (Пользователи)"])
api_router.include_router(organization.router, prefix="/organizations",
                          tags=["Organizations (Организации ТОР)"])
api_router.include_router(subunit.router, prefix="/subunits",
                          tags=["Subunits (Подразделения)"])
api_router.include_router(booking_transport.router, prefix="/booking_transport",
                          tags=["Booking images (Бронь транспорта)"])
api_router.include_router(transport.router, prefix="/transports",
                          tags=["Transport (Tранспорт)"])
api_router.include_router(order.router, prefix="/orders",
                          tags=["Orders (Заказы)"])
api_router.include_router(receipt.router, prefix="/receipts",
                          tags=["Receipts (Квитанции)"])
api_router.include_router(handler_1c_enterprise.router, prefix="/1c_enterprise",
                          tags=["Enterprise 1C (1C Предпиятие)"])
api_router.include_router(handler_erip.router, prefix="",
                          tags=["ERIP (ЕРИП)"])
api_router.include_router(pay_terminal.router, prefix="/pay_terminal",
                          tags=["Pay terminals (Терминалы)"])
