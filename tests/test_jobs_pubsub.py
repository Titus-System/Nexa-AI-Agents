import pytest
import redis
import threading
import time
from app.jobs import start_single_classification_job
from schemas.api_schemas import SingleClassificationRequest

def listen_redis_events(channel, received, stop_event, expected=3):
    r = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            received.append(message['data'])
            if len(received) >= expected:
                stop_event.set()
                break
        if stop_event.is_set():
            break
    pubsub.unsubscribe()
    pubsub.close()

@pytest.mark.integration
def test_start_single_classification_job_pubsub():
    channel = 'pytest_job_channel'
    job_id = 'job-test-pubsub'
    received = []
    stop_event = threading.Event()

    listener = threading.Thread(target=listen_redis_events, args=(channel, received, stop_event, 4))
    listener.start()
    time.sleep(0.2)

    req = SingleClassificationRequest(
        progress_channel=channel,
        partnumber='PN-123',
        description='desc',
        manufacturer='manu',
        supplier='sup'
    )
    start_single_classification_job(req, job_id)

    # Aguarda até receber todos os eventos (3 progress + 1 done)
    stop_event.wait(timeout=5)
    listener.join(timeout=2)

    assert len(received) == 4, f'Esperado 4 eventos, recebido {len(received)}.'
    assert any(b'processing' in m for m in received), 'Nenhum evento de progresso recebido.'
    assert any(b'done' in m for m in received), 'Nenhum evento de finalização recebido.'
