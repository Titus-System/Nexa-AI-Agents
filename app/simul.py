import time
from schemas.api_schemas import (
    BatchClassificationRequest,
    ProgressSchema,
    SingleClassification,
    SingleClassificationRequest,
)
from .extensions import redis_publisher


pre_proc = {
    "BC847BLT1G": SingleClassification(
        partnumber="BC847BLT1G",
        ncm="85412120",
        description="""transistores de silício NPN de uso geral, apresentados em um invólucro SOT-23. Esses componentes operam com uma corrente de coletor contínua de até 100 mAdc e possuem diferentes classificações de tensão coletor-emissor (VCEO) que variam de 30 V a 65 V, dependendo do modelo específico dentro da série. Projetados para funcionar em uma ampla faixa de temperatura de junção de -55°C a +150°C , eles oferecem uma dissipação de potência total de 225 mW em uma placa FR-5. O ganho de corrente DC (h FE), sob uma tensão de coletor-emissor de 5.0 V e uma corrente de coletor de 2.0 mA, varia entre 110 e 800, dependendo da classificação do componente. A série apresenta um produto de ganho de largura de banda (fT) de no mínimo 100 MHz em uma corrente de coletor de 10 mA.""",
        exception="00",
        nve="--",
        fabricante="ONSEMI",
        endereco="5701 North Pima Road, Scottsdale, Arizona, 85250, EUA",
        pais="CHINA, REPUBLICA POPULAR",
        confidence_score=0.95,
    ),
    "88512006119": SingleClassification(
        partnumber="88512006119",
        ncm="85322410",
        description="""capacitor cerâmico multicamadas (MLCC) da série WCAP-CSGP. É um componente de uso geral projetado para uma ampla variedade de aplicações, como acoplamento, desacoplamento e filtragem. As principais características técnicas da série incluem uma vasta gama de encapsulamentos para montagem em superfície (de 0201 a 2220), tensões nominais de 6.3V a 100V e valores de capacitância de 0.5 pF a 100 µF. Utiliza dielétricos de alta performance como NP0 (Classe I), X7R e X5R (Classe II), e opera numa faixa de temperatura de -55 °C a +125 °C.""",
        exception="00",
        nve="--",
        fabricante="Würth Elektronik".upper(),
        endereco="Max-Eyth-Straße 1, 74638 Waldenburg".upper(),
        pais="ALEMANHA",
        confidence_score=0.95,
    ),
    "CL10C330JB8NNNC": SingleClassification(
        partnumber = "CL10C330JB8NNNC",
        description = "Capacitor cerâmico multicamadas (MLCC) de 33pF, 50V, tolerância de ±5%, dielétrico C0G/NP0, encapsulamento 0603 (1608 métrico). Componente para montagem em superfície (SMD) de uso geral.",
        ncm = "85322410",
        exception = "00",
        nve = "--",
        fabricante = "Samsung Electro-Mechanics",
        endereco = "150, Maeyeong-ro, Yeongtong-gu, Suwon-si, Gyeonggi-do, República da Coreia",
        pais = "República da Coreia",
        confidence_score = 0.98
    ),

    "CL10B472KB8NNNC": SingleClassification(
        partnumber = "CL10B472KB8NNNC",
        description = "Capacitor cerâmico multicamadas (MLCC) de 4.7nF (4700pF), 50V, tolerância de ±10%, dielétrico X7R, encapsulamento 0603 (1608 métrico). Componente SMD de uso geral.",
        ncm = "85322410",
        exception = "00",
        nve = "--",
        fabricante = "Samsung Electro-Mechanics",
        endereco = "150, Maeyeong-ro, Yeongtong-gu, Suwon-si, Gyeonggi-do, República da Coreia",
        pais = "República da Coreia",
        confidence_score = 0.99
    ),
    "GRM1885C1H180JA01D": SingleClassification(
        partnumber = "GRM1885C1H180JA01D",
        description = "Capacitor cerâmico multicamadas (MLCC) de 18pF, 50V, tolerância de ±5%, dielétrico C0G/NP0, encapsulamento 0603 (1608 métrico). Componente SMD de uso geral.",
        ncm = "85322410",
        exception = "00",
        nve = "--",
        fabricante = "Murata Manufacturing Co., Ltd.",
        endereco = "10-1, Higashikotari 1-chome, Nagaokakyo-shi, Kyoto 617-8555, Japão",
        pais = "Japão",
        confidence_score = 0.99
    ),
    "CL10A106KP8NNNC": SingleClassification(
        partnumber = "CL10A106KP8NNNC",
        description = "Capacitor cerâmico multicamadas (MLCC) de 10µF, 10V, tolerância de ±10%, dielétrico X5R, encapsulamento 0603 (1608 métrico). Componente SMD de uso geral.",
        ncm = "85322410",
        exception = "00",
        nve = "--",
        fabricante = "Samsung Electro-Mechanics",
        endereco = "150, Maeyeong-ro, Yeongtong-gu, Suwon-si, Gyeonggi-do, República da Coreia",
        pais = "República da Coreia",
        confidence_score = 0.99
    ),
    "C1608X5R1E106M080AC": SingleClassification(
        partnumber = "C1608X5R1E106M080AC",
        description = "Capacitor cerâmico multicamadas (MLCC) de 10µF, 25V, tolerância de ±20%, dielétrico X5R, encapsulamento 0603 (1608 métrico). Componente SMD de uso geral.",
        ncm = "85322410",
        exception = "00",
        nve = "--",
        fabricante = "TDK Corporation",
        endereco = "2-5-1 Nihonbashi, Chuo-ku, Tóquio, 103-6128, Japão",
        pais = "Japão",
        confidence_score = 0.99
    ),
    "NACE100M100V6.3X8TR13F": SingleClassification(
        partnumber = "NACE100M100V6.3X8TR13F",
        description = "Capacitor eletrolítico de alumínio de 10µF, 100V, tolerância de ±20%, tipo V-Chip para montagem em superfície (SMD). Faixa de temperatura de -40°C a +85°C.",
        ncm = "85322200",
        exception = "00",
        nve = "--",
        fabricante = "NIC Components Corp.",
        endereco = "1 Huntington Quadrangle, Suite 1C10, Melville, NY 11747, EUA",
        pais = "EUA",
        confidence_score = 0.95
    ),
    "CRCW060320K0FKEA": SingleClassification(
        partnumber = "CRCW060320K0FKEA",
        description = "Resistor de filme espesso de 20kΩ, 0.125W (1/8W), tolerância de ±1%, encapsulamento 0603. Componente SMD com qualificação automotiva AEC-Q200.",
        ncm = "85332190",
        exception = "00",
        nve = "--",
        fabricante = "Vishay Dale",
        endereco = "63 Lancaster Avenue, Malvern, PA 19355-2143, EUA",
        pais = "EUA",
        confidence_score = 0.98
    ),
    "ERJ-2RKF2201X": SingleClassification(
        partnumber = "ERJ-2RKF2201X",
        description = "Resistor de filme espesso de precisão de 2.2kΩ, 0.1W (1/10W), tolerância de ±1%, encapsulamento 0402 (1005 métrico). Componente SMD de grau automotivo.",
        ncm = "85332190",
        exception = "00",
        nve = "--",
        fabricante = "Panasonic",
        endereco = "1006, Kadoma, Kadoma City, Osaka 571-8501, Japão",
        pais = "Japão",
        confidence_score = 0.98
    ),
    "IRLML6401TRPBF": SingleClassification(
        partnumber = "IRLML6401TRPBF",
        description = "Transistor MOSFET de Canal P, -12V, -4.3A, com baixa resistência de condução (RDS(on)) de 50mΩ (máx) a VGS = -4.5V. Encapsulamento SOT-23. Projetado para acionamento por nível lógico.",
        ncm = "85412120",
        exception = "00",
        nve = "--",
        fabricante = "Infineon Technologies",
        endereco = "Am Campeon 1-15, 85579 Neubiberg, Alemanha",
        pais = "Alemanha",
        confidence_score = 0.98
    ),
    "STPS5H100B-TR": SingleClassification(
        partnumber = "STPS5H100B-TR",
        description = "Diodo retificador Schottky de alta tensão, 100V, 5A. Baixa queda de tensão direta (730mV @ 5A). Encapsulamento DPAK (TO-252).",
        ncm = "85411029",
        exception = "00",
        nve = "--",
        fabricante = "STMicroelectronics",
        endereco = "39 Chemin du Champ-des-Filles, 1228 Plan-les-Ouates, Genebra, Suíça",
        pais = "Suíça",
        confidence_score = 0.98
    ),
    "ESD7C3.3DT5G": SingleClassification(
        partnumber = "ESD7C3.3DT5G",
        description = "Diodo de supressão de tensão transiente (TVS) para proteção contra ESD. Tensão de trabalho de 3.3V, 2 canais unidirecionais. Encapsulamento SOT-723. Qualificação automotiva AEC-Q101.",
        ncm = "85411029",
        exception = "00",
        nve = "--",
        fabricante = "onsemi",
        endereco = "5701 North Pima Road, Scottsdale, AZ 85250, EUA",
        pais = "EUA",
        confidence_score = 0.98
    ),
    "LD1117ADT-TR": SingleClassification(
        partnumber = "LD1117ADT-TR",
        description = "Regulador de tensão linear de baixa queda (LDO), positivo, ajustável (1.25V a 15V), com capacidade de corrente de até 1A. Encapsulamento DPAK.",
        ncm = "85423919",
        exception = "00",
        nve = "--",
        fabricante = "STMicroelectronics",
        endereco = "39 Chemin du Champ-des-Filles, 1228 Plan-les-Ouates, Genebra, Suíça",
        pais = "Suíça",
        confidence_score = 0.99
    ),
    "ECS-3225Q-33-260-BS-TR": SingleClassification(
        partnumber = "ECS-3225Q-33-260-BS-TR",
        description = "Oscilador de cristal SMD, 26 MHz, saída HCMOS, alimentação de 3.3V. Estabilidade de frequência de ±50ppm na faixa de temperatura de -40°C a +125°C. Encapsulamento 3.2mm x 2.5mm. Qualificação AEC-Q200.",
        ncm = "85416090",
        exception = "00",
        nve = "--",
        fabricante = "ECS Inc. International",
        endereco = "15351 West 109th Street, Lenexa, KS 66219, EUA",
        pais = "EUA",
        confidence_score = 0.98
    )
}


messages = {
    0: "Pedido de análise recebido",
    1: "Iniciando análise de partnumber com agente Nexa-IA",
    2: "Buscando informações técnicas do partnumber",
    3: "Buscando informações técnicas do partnumber",
    4: "Gerando descrição do produto",
    5: "Finalizando descrição do produto"
}

def run_single_simul(data: SingleClassificationRequest, job_id: str):
    print(f"Iniciando job para partnumber {data.partnumber} no canal {data.progress_channel}")

    try:
        if data.partnumber not in pre_proc.keys():
            redis_publisher.send_failed_processing(data.progress_channel, "Partnumber não encontrado na base de dados de simulação")

        for i in range(6):
            progress_schema = ProgressSchema(
                current=i, total=5, message=messages.get(i)
            )
            redis_publisher.send_progress_update(data.progress_channel, progress_schema)
            if i < 6: time.sleep(4)
            else: time.sleep(3)

        time.sleep(5)
        result = pre_proc[data.partnumber]
        redis_publisher.send_done_classification(data.progress_channel, result, job_id)
        return result

    except Exception as e:
        redis_publisher.send_failed_processing(data.progress_channel, str(e))
    return


def run_batch_simul(data: BatchClassificationRequest, job_id: str):
    print(f"Iniciando job para classificação dos partnumbers: {data.partnumbers} no canal {data.progress_channel}")
    total = len(data.partnumbers)
    partnumbers = [i for i in data.partnumbers.keys()]
    for i in range(total):
        p = partnumbers[i]
        try:
            redis_publisher.send_progress_update(
                data.progress_channel,
                ProgressSchema(current=i, total=total, message=f"[{i}] Processando partnumber {p} com Nexa IA")
            )
            result = pre_proc.get(p, None)
            time.sleep(2)
            if result is not None:
                redis_publisher.send_partial_result(
                    channel = data.progress_channel,
                    job_id = job_id,
                    result = result,
                    current = i,
                    total = total,
                    message = f"Classificação encontrada para o partnumber {p}"
                )
            time.sleep(3)
        except Exception as e:
            print(f"Erro ao processar classificação do partnumber {p}")
            pass
    redis_publisher.send_done_job(channel=data.progress_channel, job_id=job_id)
    return
