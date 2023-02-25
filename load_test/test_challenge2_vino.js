import http from 'k6/http';
import { check, sleep } from 'k6';

const requestBody = open('./req.json');

export const options = {
    vus: 20,
    duration: '1m'
};

export default function () {
    const options  = { headers: {"content-type": "application/json"} };
    const result = http.post('http://localhost:9001/v1/models/challenge2:predict', requestBody, options);

    check(result, (r) => r.status === 200);

    sleep(1);
}
