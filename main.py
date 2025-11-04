import flet as ft
import config
import data
from Utilities.auth_buttons_actions import (SignUp_Btn, SignIn_Btn)
from Utilities.review_button_actions import ReviewUs_Action_Btn
from Utilities.common import Close_Popup
from Database.auth import Auth_DB
from Database.shipment import Get_Parcel_Info



def Traking_shipment_Btn(e):
    def Tracking(e):
        shipment_id.error_text = None

        if not shipment_id.value:
            shipment_id.error_text = "Please enter shipment id"
        else:
            shipment_details = Get_Parcel_Info(shipment_id.value)
            if not shipment_details:
                shipment_id.error_text = "Invalid shipment id"

        if shipment_id.error_text:
            e.page.update()
            return

        email, from_name, to_name, to_address, parcel_id, parcel_type, parcel_quantity, parcel_weight, from_board, to_board, km, amount, pickup_date, drop_date, status = shipment_details


        # Define the dialog
        shipment_infos_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Tracked Shipment Details", size=20, weight="bold"),
            content=ft.Column(
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    title=ft.Text(f"Shipment (Parcel ID): {parcel_id}", size=20, weight="bold"),
                                ),
                                ft.ListTile(
                                    title=ft.Text(
                                        f"""Sender Name: {from_name}
Receiver Name: {to_name}
Receiver Address: {to_address}
Shipment Scheduled: {pickup_date.strftime("%d-%m-%Y")}
Shipment Delivered: {drop_date.strftime("%d-%m-%Y") if drop_date else 'Not Yet Delivered'}
Parcel Type: {parcel_type}
Parcel Weight (1 Parcel): {parcel_weight} kg
Parcel Quantity: {parcel_quantity}
Distance: {km} km
Total Charges: ₹{amount}
Status: {status}"""
                                    ),
                                ),
                                ft.ListTile(
                                    title=ft.Text(f"Boading Place\nFrom: {from_board} -> To: {to_board}"),
                                    trailing=ft.Text(f"Booked By: \"{email}\""),
                                ),
                            ],
                            spacing=5,
                        ),
                        padding=ft.padding.all(10),
                    )
                ),
            ],
            spacing=15,
        ),
            actions=[
                ft.TextButton("Close",on_click=lambda e: Close_Popup(e.page, shipment_infos_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Display the dialog
        Close_Popup(e.page, shipment_track_popup)
        e.page.open(shipment_infos_dialog)

    shipment_track_popup = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Tracking Shipment"),
            content=ft.Column(
                [
                    ft.Text("Enter the 8 digit Shipment ID(Parcel ID) ,"),
                    ft.Text("to gather latest infromations about the shipment"),
                    shipment_id := ft.TextField(label="Shipment's Code", max_length=8,input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                ],tight=True,
            ),
            actions=[
                ft.TextButton("Track Shipment", on_click=Tracking),
                ft.TextButton("Cancel",on_click=lambda e: Close_Popup(e.page, shipment_track_popup)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    e.page.open(shipment_track_popup)

def Main_Page(page):
    # Set the title
    page.title = config.SERVICE_NAME

    data.PAGE = page
    page.scroll = ft.ScrollMode.AUTO
    # Add the layout to the page
    page.add(
        ft.Container(
            padding=ft.Padding(top=250, left=0, right=0, bottom=0),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            # Welcome message
                            ft.Text(
                                spans=[
                                    ft.TextSpan(
                                        f"Welcome, to our {config.SERVICE_NAME}!",
                                        ft.TextStyle(
                                            size=40,
                                            weight=ft.FontWeight.BOLD,
                                            foreground=ft.Paint(
                                                gradient=ft.PaintLinearGradient(
                                                    (0, 20), (150, 20), 
                                                    [ft.Colors.RED, ft.Colors.YELLOW]
                                                )
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Text(f"\"Fast and secure courier service for timely deliveries.\""),
                    ft.Text(""),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.TextButton(
                                "Sign-In",
                                icon="LOGIN_OUTLINED",
                                icon_color=ft.Colors.GREEN,
                                on_click=SignIn_Btn,
                            ),
                            ft.TextButton(
                                "Sign-Up",
                                icon="FOLLOW_THE_SIGNS_ROUNDED",
                                icon_color=ft.Colors.GREEN,
                                on_click=SignUp_Btn,
                            ),
                            ft.TextButton(
                                "Track Shipment",
                                icon="MY_LOCATION_ROUNDED",
                                icon_color=ft.Colors.ORANGE,
                                on_click=Traking_shipment_Btn,
                            ),
                            ft.TextButton(
                                "Review Us",
                                icon="REVIEWS_OUTLINED",
                                icon_color=ft.Colors.BLUE_500,
                                on_click=ReviewUs_Action_Btn,
                            ),
                        ],
                    ),
                ],
            ),
        )
    )
    return

def main(page: ft.Page):
    Auth_DB()

    Main_Page(page)
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)