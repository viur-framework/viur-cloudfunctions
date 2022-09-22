# viur-cloudfunctions

## thumbnailer

### Usage
1.  Clone this repository with `git clone https://github.com/viur-framework/viur-cloudfunctions.git`
    > This creates a new local folder `viur-cloudfunctions`.
    
2. `cd viur-cloudfunctions/thumbnailer`

3. Add your hmacKey (`conf["viur.file.hmacKey"]`)  from your `main.py` in the `env.yaml`
    >If you don't have a hmac key yet you must create these  and write it in the `main.py` and in the `env.yaml`
    
4. Deploy your cloud function with `sh ./deploy.sh`


## Contributing

ViUR is developed and maintained by [Mausbrand Informationssysteme GmbH](https://www.mausbrand.de/en), from Dortmund in Germany. We are a software company consisting of young, enthusiastic software developers, designers and social media experts, working on exciting projects for different kinds of customers. All of our newer projects are implemented with ViUR, from tiny web-pages to huge company intranets with hundreds of users.

Help of any kind to extend and improve or enhance this project in any kind or way is always appreciated.

We take great interest in your opinion about ViUR. We appreciate your feedback and are looking forward to hear about your ideas. Share your vision or questions with us and participate in ongoing discussions.

## License

Copyright © 2022 by Mausbrand Informationssysteme GmbH.<br>
Mausbrand and ViUR are registered trademarks of Mausbrand Informationssysteme GmbH.

You may use, modify and distribute this software under the terms and conditions of the GNU Lesser General Public License (LGPL). See the file LICENSE provided within this package for more information.
