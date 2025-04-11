# Guía de Inicio Rápido

Esta guía te ayudará a poner en marcha el proyecto de Data Lake para la comercializadora de energía.

## Prerrequisitos

### 1. AWS CLI
```bash
# macOS (con Homebrew)
brew install awscli

# Configurar AWS CLI
aws configure
```

### 2. Terraform
```bash
# macOS (con Homebrew)
brew install terraform
```

### 3. Python y dependencias
```bash
# Instalar Python 3.8+
brew install python

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración Inicial

### 1. Variables de Terraform

Crea un archivo `terraform.tfvars` en `infrastructure/terraform/`:

```hcl
aws_region = "us-east-1"
environment = "dev"
project_name = "energy-trading"
data_lake_bucket_name = "tu-empresa-datalake-dev"
athena_output_bucket = "tu-empresa-athena-results-dev"
redshift_master_password = "TuContraseñaSegura123!"
```

### 2. Despliegue de Infraestructura

```bash
# Inicializar Terraform
cd infrastructure/terraform
terraform init

# Validar configuración
terraform plan

# Desplegar infraestructura
terraform apply
```

### 3. Configuración de AWS Lake Formation

1. Accede a la consola de AWS
2. Ve a Lake Formation
3. Configura los administradores:
   - Ve a "Administrative roles and tasks"
   - Agrega tu usuario como administrador

## Carga de Datos

### 1. Datos de Ejemplo
Los datos de ejemplo ya están incluidos en:
- `data/raw/providers/sample_providers.csv`
- `data/raw/clients/sample_clients.csv`
- `data/raw/transactions/sample_transactions.csv`

### 2. Cargar datos a S3
```bash
# Asumiendo que estás en la raíz del proyecto
aws s3 cp data/raw/providers/sample_providers.csv s3://tu-empresa-datalake-dev/raw/providers/$(date +%Y-%m-%d)/
aws s3 cp data/raw/clients/sample_clients.csv s3://tu-empresa-datalake-dev/raw/clients/$(date +%Y-%m-%d)/
aws s3 cp data/raw/transactions/sample_transactions.csv s3://tu-empresa-datalake-dev/raw/transactions/$(date +%Y-%m-%d)/
```

## Ejecución de Jobs

### 1. AWS Glue

1. Ejecutar el crawler:
```bash
aws glue start-crawler --name energy-trading-raw-crawler
```

2. Esperar a que el crawler termine y ejecutar el job de transformación:
```bash
aws glue start-job-run --job-name raw-to-processed
```

### 2. Consultas con Athena

1. Configurar el bucket de salida en Athena:
```python
# Usar el script de ejemplo
python scripts/python/athena_queries.py
```

## Monitoreo

### 1. CloudWatch Logs
- Revisar los logs de Glue en CloudWatch Logs
- Namespace: `/aws-glue/jobs/`

### 2. Métricas
- Acceder a CloudWatch Metrics
- Namespace: `AWS/Glue`

## Troubleshooting

### 1. Problemas comunes

#### Error de permisos en S3
```bash
# Verificar política de bucket
aws s3api get-bucket-policy --bucket tu-empresa-datalake-dev
```

#### Fallos en jobs de Glue
```bash
# Ver logs del job
aws logs get-log-events --log-group-name /aws-glue/jobs/raw-to-processed --log-stream-name <stream-name>
```

### 2. Verificación de estado

#### Estado del crawler
```bash
aws glue get-crawler --name energy-trading-raw-crawler
```

#### Estado del job
```bash
aws glue get-job-run --job-name raw-to-processed --run-id <run-id>
```

## Siguientes Pasos

1. **Personalización**
   - Ajustar parámetros de transformación
   - Modificar esquemas según necesidades
   - Agregar transformaciones adicionales

2. **Automatización**
   - Configurar triggers de Glue
   - Implementar pipelines de CI/CD
   - Automatizar pruebas

3. **Monitoreo**
   - Configurar alertas
   - Crear dashboards
   - Implementar logging detallado

## Recursos Adicionales

- [Documentación de Arquitectura](./ARCHITECTURE.md)
- [AWS Glue Documentation](https://docs.aws.amazon.com/glue)
- [AWS Lake Formation Documentation](https://docs.aws.amazon.com/lake-formation)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws) 