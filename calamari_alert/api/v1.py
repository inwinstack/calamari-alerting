

class UserManager(object):

    def user_info(self):
        url = self._url(1, 'user/me')
        response, body = self._get(url, body='json')
        return body

    def alert_rule(self):
        url = self._url(1, 'user/me/alert_rule')
        response, body = self._get(url, body='json')
        return body


class ClusterManager(object):

    def __init__(self):

        self.cluster_id = None
        self.cluster_update_time = None
        self.cluster_update_time_unix = None
        self.name = None
        self.clusters = None

    def cluster_list(self):
        url = self._url(1, 'cluster')
        response, body = self._get(url, body='json')

        if isinstance(body, list):
            self.clusters = []
            for cluster in body:
                self.clusters.append({'cluster_id': cluster['id']})

    def cluster_detail(self, index):
        url = self._url(1, 'cluster/' + self.clusters[index]['cluster_id'])
        response, body = self._get(url, body='json')
        self._get_cluster_info(body)

    def first_cluster_detail(self):
        url = self._url(1, 'cluster/' + self.clusters[0]['cluster_id'])
        response, body = self._get(url, body='json')
        self._get_cluster_info(body)

    def _get_cluster_info(self, body):
        if isinstance(body, dict):
            self.cluster_id = body['id']
            self.cluster_update_time = body['cluster_update_time']
            self.cluster_update_time_unix = body['cluster_update_time_unix']
            self.name = body['name']


class HealthManager(object):

    def health_counters(self, cluster_id):
        url = self._url(1, 'cluster/{0}/health_counters'.format(str(cluster_id)))
        response, body = self._get(url, body='json')
        return body if isinstance(body, dict) else None


class SpaceManager(object):

    def cluster_space(self, cluster_id):
        url = self._url(1, 'cluster/{0}/space'.format(str(cluster_id)))
        response, body = self._get(url, body='json')

        return body if isinstance(body, dict) else None