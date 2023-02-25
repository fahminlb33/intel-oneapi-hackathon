# Intel® oneAPI Hackathon for Open Innovation

By: Kodesiana (Fahmi Noor Fiqri)

You can find the specific documentation and how-to in the specific challenge directory.

* [Challenge 1 - Machine Learning Challenge Track: Predict the quality of freshwater](./challenge1)
* [Challenge 2 - Computer Vision Challenge Track: Target and Eliminate](./challenge2)

## Running the App

Instead of following the specific guidelines above, you can run all the app from this root project directory using Docker Compose!

```bash
$ git clone --recurse-submodules https://github.com/fahminlb33/intel-oneapi-hackathon

$ cd intel-oneapi-hackathon

$ bash ./challenge2/download_model.sh

$ docker-compose up
```

After the all the container are running, you can open http://localhost:8000 to visit the app homepage.

### Postman Collection

You can access the Postman collection [here](./kodesiana.postman_collection.json). Don't forget you need a running server before using this API collection.

## License

Licensed under Apache License 2.0
