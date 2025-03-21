import pika
import json


# 간단한 자격 증명 확인 함수 (예제용으로 하드코딩)
def check_credentials(username, password):
    # 실제 환경에서는 데이터베이스나 인증 서비스를 사용해야 함
    return username == "user" and password == "pass"


# 메시지 처리 콜백 함수
def on_request(ch, method, props, body):
    try:
        # 수신된 메시지 출력
        print(f"새 메시지 수신: {body.decode('utf-8')}")

        # 수신된 메시지 바이트를 UTF-8로 디코딩하고 JSON 파싱
        data = json.loads(body.decode('utf-8'))
        username1 = data['username1']
        password1 = data['password1']
        username2 = data['username2']
        password2 = data['password2']

        # 파싱된 자격 증명 정보 출력
        print(f"처리 중인 자격 증명: 사용자1={username1}, 사용자2={username2}")

        # 두 세트의 자격 증명 확인
        if check_credentials(username1, password1) and check_credentials(username2, password2):
            response = "성공"  # Spring Boot에서 기대하는 성공 응답
            print("인증 결과: 성공")
        else:
            response = "실패"  # 실패 응답
            print("인증 결과: 실패")

        # 응답 메시지 전송
        ch.basic_publish(
            exchange='',
            routing_key='login-check-response-queue',  # 응답 큐
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id  # 요청과 동일한 correlation ID 사용
            ),
            body=response.encode('utf-8')  # 응답을 바이트로 인코딩
        )
        print(f"응답 전송 완료: {response}")

        # 메시지 처리 완료 확인
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"메시지 처리 중 오류 발생: {e}")
        # 오류 발생 시 메시지 재처리 가능하도록 NACK
        ch.basic_nack(delivery_tag=method.delivery_tag)


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
    channel = connection.channel()

    print("연결 성공!")  # RabbitMQ 연결 설정

    # 큐 선언 (Spring Boot와 동일한 큐 이름 사용)
    channel.queue_declare(queue='login-check-request-queue')
    channel.queue_declare(queue='login-check-response-queue')

    # 소비자 설정
    channel.basic_consume(
        queue='login-check-request-queue',  # 요청 큐에서 메시지 수신
        on_message_callback=on_request
    )

    print("메시지를 기다리는 중입니다. 종료하려면 CTRL+C를 누르세요.")
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError as e:
    print(f"연결 실패: {e}")