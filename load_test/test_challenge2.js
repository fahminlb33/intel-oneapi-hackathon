import http from 'k6/http';
import { check, sleep } from 'k6';

const imageFile = open('./agri_0_39.jpeg', 'b');

export const options = {
    vus: 20,
    duration: '1m',
};

export default function () {
    const data = {file: http.file(imageFile, 'agri_0_39.jpeg', 'image/jpeg')};
    const result = http.post('http://localhost:8002/predict', data);

    check(result, (r) => r.status === 200);

    sleep(1);
}