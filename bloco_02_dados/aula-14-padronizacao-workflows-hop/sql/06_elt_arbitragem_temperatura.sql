-- ============================================================================
-- sql/06_elt_arbitragem_temperatura.sql
-- FIC Engenharia de Dados | Aula 03 (Módulo 2)
-- Motor de Arbitragem e Reconciliação de Temperatura (INMET vs CPTEC/INPE)
-- ============================================================================

-- 1. Identifica e envia anomalias do sensor físico INMET para a Quarentena
INSERT INTO silver.rejeitados (pipeline_origem, motivo_erro, registro_bruto, data_rejeicao)
SELECT 
    'reconciliacao_temperatura_arbitragem' AS pipeline_origem,
    CONCAT('Leitura física do sensor INMET implausível ou fora da faixa térmica permitida (', i.temperatura_c, '°C)') AS motivo_erro,
    CONCAT('{"cod_mun_6":"', i.cod_mun_6, '","municipio":"', i.municipio, '","temperatura_c":"', i.temperatura_c, '","status_sensor":"', i.status_sensor, '"}') AS registro_bruto,
    CURRENT_TIMESTAMP AS data_rejeicao
FROM staging.inmet_temperatura i
WHERE NULLIF(TRIM(i.temperatura_c), '') IS NOT NULL 
  AND NULLIF(TRIM(i.temperatura_c), '')::NUMERIC NOT BETWEEN -10.0 AND 50.0;

-- 2. Executa a Reconciliação (Golden Record) com Fallback Automático
INSERT INTO silver.clima_reconciliado (
    cod_mun_6,
    municipio,
    temp_inmet_original,
    temp_cptec_original,
    temperatura_eleita,
    fonte_eleita,
    status_arbitragem
)
SELECT 
    c.cod_mun_6,
    c.municipio,
    NULLIF(TRIM(i.temperatura_c), '')::NUMERIC AS temp_inmet_original,
    NULLIF(TRIM(c.temperatura_satelite_c), '')::NUMERIC AS temp_cptec_original,
    
    -- REGRA DE SELEÇÃO: Se INMET válido (-10°C a 50°C), elege INMET; senão faz Fallback para CPTEC
    CASE 
        WHEN NULLIF(TRIM(i.temperatura_c), '') IS NOT NULL 
             AND NULLIF(TRIM(i.temperatura_c), '')::NUMERIC BETWEEN -10.0 AND 50.0
        THEN NULLIF(TRIM(i.temperatura_c), '')::NUMERIC
        ELSE NULLIF(TRIM(c.temperatura_satelite_c), '')::NUMERIC
    END AS temperatura_eleita,
    
    -- FONTE ELEITA
    CASE 
        WHEN NULLIF(TRIM(i.temperatura_c), '') IS NOT NULL 
             AND NULLIF(TRIM(i.temperatura_c), '')::NUMERIC BETWEEN -10.0 AND 50.0
        THEN 'INMET_TERRESTRE'
        ELSE 'CPTEC_SATELITE'
    END AS fonte_eleita,
    
    -- STATUS AUDITÁVEL DA ARBITRAGEM
    CASE 
        WHEN NULLIF(TRIM(i.temperatura_c), '') IS NULL OR TRIM(i.temperatura_c) = ''
        THEN 'Fallback acionado: Sensor físico INMET ausente/offline -> Utilizado satélite CPTEC'
        
        WHEN NULLIF(TRIM(i.temperatura_c), '')::NUMERIC NOT BETWEEN -10.0 AND 50.0
        THEN CONCAT('Fallback acionado: Leitura INMET anômala (', i.temperatura_c, '°C) isolada na Quarentena -> Utilizado satélite CPTEC')
        
        ELSE 'Arbitragem nominal: Leitura física do INMET consistente e validada como Golden Record'
    END AS status_arbitragem

FROM staging.cptec_temperatura c
LEFT JOIN staging.inmet_temperatura i ON c.cod_mun_6 = i.cod_mun_6
ON CONFLICT (cod_mun_6) DO UPDATE 
SET temp_inmet_original = EXCLUDED.temp_inmet_original,
    temp_cptec_original = EXCLUDED.temp_cptec_original,
    temperatura_eleita = EXCLUDED.temperatura_eleita,
    fonte_eleita = EXCLUDED.fonte_eleita,
    status_arbitragem = EXCLUDED.status_arbitragem,
    data_processamento = CURRENT_TIMESTAMP;
