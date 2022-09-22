# viur-cloudfunctions

## thumbnailer

### Usage
1.  Clone this repository with `git clone https://github.com/viur-framework/viur-cloudfunctions.git`
    > This creates a new local folder `viur-cloudfunctions`.
    
2. `cd viur-cloudfunctions/thumbnailer`

3. Add your hmacKey (`conf["viur.file.hmacKey"]`) and Secrect Key (`conf["viur.file.thumbnailer_secKey"]`) from your `main.py` in the `env.yaml`
    >If you don't have a secret or hmac key yet you must create these two and write they in the `main.py` and in the `env.yaml`
    
4. Deploy your cloud function with `sh ./deploy.sh`
