import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    vus: 20,
    duration: '1m',
};

export default function () {
    const data = {
        "single": [
            7.258203145845717,
            6.107129837217062e-09,
            9.26167580122401,
            182.2423407530417,
            4.3998520479124295e-224,
            0.4164775464847408,
            2, // parameters.py#COLOR_MAP
            0.0478031791644083,
            1.0161962374839366,
            0.2980934209430296,
            3.1441986515867457,
            114.55142662349748,
            160.06255735415195,
            2.3250939237169903,
            6.020679600903066e-16,
            214.5531038247008,
            1,// parameters.py#SOURCE_MAP
            15.891904856714174,
            61.13914033047329,
            1,// parameters.py#MONTH_MAP
            11.0,
            4.0
        ]
    };
    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const result = http.post('http://localhost:8001/predict', JSON.stringify(data), params);
    check(result, (r) => r.status === 200);

    sleep(1);
}
