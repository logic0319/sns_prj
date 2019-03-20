from pyfcm import FCMNotification

__all__ = ('messaging', )


def messaging(message_body, post_pk, registration_id):
    data_message = {
        "post_pk": post_pk,
    }
    message_title = "패롯의 알림"
    api_key = "AAAAH9L9RaI:APA91bGPaj0u1ETZd42p7FDUac4Yz2Y8h02TmxvVKIx0hxPfnE4ZGI72-7c7SkkjT84ItTo1VHDiEfo9s-GW5uQ2d6SLmJhhztnuppM0mssxXKJNVRnv-anwum_UyCPpMV1r0aFaOJfmOg93mN1SJrepGKFPruk1hw"
    push_service = FCMNotification(api_key=api_key)
    push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                      message_body=message_body, data_message=data_message, )