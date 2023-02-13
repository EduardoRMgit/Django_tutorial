import base64
import environ


def cluster_secret(key, value):
    try:
        from kubernetes import client, config
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        secret = v1.read_namespaced_secret(key, 'default')
        secret = base64.b64decode(secret.data[value]).decode('utf-8')
    except Exception:
        env = environ.Env()
        secret = env.str(value, 'a')
    return secret
