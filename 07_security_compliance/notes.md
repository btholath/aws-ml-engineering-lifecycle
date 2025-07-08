

***Why & How to secure SageMaker applications ?***

<pre>
from sagemaker import get_execution_role, Session

role = get_execution_role()
sagemaker_session = Session()

vpc_config = {
    'SecurityGroupIds': ['sg-xxxxxx'],
    'Subnets': ['subnet-xxxxxx']
}

predictor = model.deploy(
    instance_type='ml.m4.xlarge',
    endpoint_name='secured-endpoint',
    vpc_config_override=vpc_config
)
</pre>