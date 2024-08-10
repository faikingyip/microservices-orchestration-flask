
# Stores subsystem

## Description

An example microservices application orchestration code written in Flask.

The application allows retrieval of store information and to determine nearest stores from postcode.


## Project structure

* src/adapters - This folder facilitates abstractions. The name adapter is chosen because the functionality here acts as adapters for "ports" specified in the application. For example, we use the repository pattern, which abstracts away the detail of data access. The concrete repos are the adapters. We currently only have repository classes. However, there may be a need to extend with different types of adapters, i.e. message queue publishers, notifications, etc.

* src/domain - This is where all the domain logic lives and will be encapsulated. In our case, we needed a formula to calculate the distance between 2 points. This formula would have been agreed with the business prior to implementation. As we introduce new domain rules and constraints, these will be encapsulated within this folder. As part of domain driven design, this is the most important folder and the entities with must reflect the problem domain as accurately as possible. By segregating domain logic, we can clearly focus on it.

* src/entrypoints - This folder houses the possible entrypoints into our application. For example, flask exposes endpoints that external callers can connect. If this project had to implement message listeners, then these listeners would also be placed here.

* src/srv_layer - This is our service layer folder. The functionality here is exposed to the entrypoints and will hide details such as data access sources used. This way, the responsibility of the calling code, i.e. the routes, can be to make requests to a services in a simple manner.

* app.py - This is a standard file in Flask. However, the routes have been moved into entrypoints as the number of routes may grow over time. app.py continues to exist because it is the initial setup of a flask application and will be referenced in several places.

* main.py - This is the file used to run the Flask application on the server. Its job is to bootstrap the application, providing the configuration required to configure the application. The bootstrapping can be used in different places to provide the configuration for their respective running modes, i.e. test. As a result, an improvement could be to encapsulate the bootstrapping code into a function, i.e. create_app().


## Instructions to run

1) Navigate to the root folder.

2) Build the image and container:

```
docker compose build
```

3) Run the tests:
```
docker compose run --rm app sh -c "pytest -s"
```

4) Start the application
```
docker compose up
```

5) Navigate to http://127.0.0.1:5000 to view the list of stores. For testing purposes, you can also navigate to http://127.0.0.1:5000/nearby/ to see the list of nearby stores within a 30km radius of the postcode "CM20 1FE".


## SUMMARY

* Using well known design patterns is a good approach because they are universally understood. This means less documentation and ultimately leads to code that is more maintainable.

* The Unit of Work pattern is also useful in situations where we need to perform mutating transactions. In these cases, the Unit of Work can be employed to abstract away the detail of managing transactions, again, making the code easier to test. Given that the operations in this subsystem are queries and there are no mutations, I didn't employ the Unit of Work pattern. However, the standard implementation of UoW is that it will have a reference to the repository and we'd access the repository from there rather than directly. This means, if we later decide to employ UoW we'd need to update our references to the repository.

* Beautifulsoup and Requests were libraries used to as part of automated tests. However, we won't need these libraries in production. So an enhancement would be to take steps to ensure beautifulsoup is only installed during development and testing, and is removed in production.

* There will always be areas of improvement and this will become more apparent as the project evolves. However, the architecture at its currently form has been designed to make refactoring easier.

* Exception handling was not employed for the most part of this project and is usually implemented and tested as part of development. An enhancement would be to create custom exceptions that are not bound to any particular layer in the architecture. This way, any part of the functionality below the entrypoints can raise the error and the entrypoint functionalities will be able to catch the specific custom errors. Any unanticipated errors will be caught by a middleware so that some logging can be used to make maintainers aware of them. This approach will allow us to freely raise exceptions at any point and the entrypoints will be able to catch the known ones.



# MY THOUGHT PROCESS

## 1) FIRST - Create a Docker container with a new Python-based application. Any framework is fine, we prefer Flask.

* Create a Flask application
* Containerize the application

### 1.1) Create a Flask application
* Create a virtual environment, which will contain only the dependancies we need.
* Used the standard .gitignore for python projects provided on git hub.
* In addition to the Flask library, I also added the pytest library in prep for testing. All library versions will be fixed in order to avoid surprises.
* Initially created the src and tests folders at the root of the project. This allows readiness to write tests in addition to the source code. I will take a TDD approach for this application.
* An app.py is created under src to start with, just to get things going. The location of this file may change later as the architecture evolves.


### 1.2) Containerize the application
* Created a dockerfile and .dockerignore
* Created a compose.yaml file so we can manage our container more easily using docker compose. The following commands can be used:
  * docker compose build
  * docker compose up
  * docker compose down
* Use the following to run pytest inside the docker container:
  * docker compose run --rm app sh -c "pytest -s"


## 2) SECOND - Backend Software Engineer tasks

* Render the list of stores from the `stores.json` file in alphabetical order using a template.
* Use [Postcodes.io](https://postcodes.io) to get the latitude and longitude for each postcode. Render them next to each store location in the template.
* Build the functionality that allows you to return a list of stores in a given radius of a given postcode in the UK. The list must be ordered from north to south. No need to render anything, but the function needs to be unit tested.


### 2.1) Render the list of stores from the stores.json file in alphabetical order using a template.
* Approach
* Write tests and basic implementation
* Refactor implementation and tests

#### 2.1.1) Approach
* The url to retrieve all the stores will be / for convenience.

* The list of stores is conveniently provided in a stores.json file. However, this may not always be the case and we need to ensure that we can easily swap out store.json for another store such as a database when the time comes. The proposed approach is to use the Repository Pattern to abstract away the concrete store that is being used. This way, we can easily swap out one concrete store for another and the calling code would not need any knowledge of it. Furthermore, the ability to easily swap out concrete implementations will make our code easier to test.

* In classic OOP the Repository Pattern is implemented by defining an Abstract Repository that provides the abstract methods for data access. We then subclass and implement the abstract methods. In Python, you can achieve the same effect by duck typing, however I'd go with the OOP style as this is an important pattern that defines our architecture so we should be formal and explicit about the pattern in use.

* What should the repository return? It is easy to convert the contents if the file into a standard python dict, but is this the correct approach given an alternative is to reconstitute a domain model representation from the data? The argument for returning as dict is that the data will be retrieved for read only purposes. We do not need to have any business logic at this stage so a domain model representation will complicate things. Dict it is!


#### 2.1.2) Write tests and basic implementation 
* The implementation stage will be short cycles of writing tests first, then provide a basic implementation to pass the tests. Once the tests have passed, I can refactor in the direction of the mentioned approach, refactoring the tests as well to match the design. This approach is crucial as it means asserting our expectations of what we'd expect the behaviour to be rather than to let the behaviour lead our expectations.

* What kinds of tests should we perform? We can perform end to end tests, which means testing the api endpoint and all the real underlying components. We can write integration tests, which tests the interaction between a specific set of components. Or we can write unit tests. In this case, we can go ahead and write the end to end test only, given our endpoints do not mutate any data and that the data is held within a file. The e2e tests will also invoke the functionality of the underlying components, which means we would benefit less from writing unit tests and integrations tests. This will also make refactoring easier as there will be fewer tests to update.


#### 2.1.3) Refactor implementation and tests
The repository serves as an abstraction to the store. Its role can be categorized as an adapter to the datasource. To this end, I created a folder called "adapters" to house the repository code. The code that extracts stores information from the file will be placed in there. As the only tests performed at this stage are e2e, we should observe no refactoring necessary in our tests.




### 2.2) Use Postcodes.io to get the latitude and longitude for each postcode. Render them next to each store location in the template.
* Approach
* Write tests and basic implementation
* Refactor implementation and tests


#### 2.2.1) Approach
* The requirement to display the latitude and longitude for each store can be considered an enhancement to 2.1). We need to aggregate extra data with the existing data. The source for the latitude and longitude is Postcodes.io, which provides a POST endpoint at https://api.postcodes.io/postcodes, where we can submit a list of postcodes as the body. This will be useful but it is important to test if there are any limits imposed on the number of postcodes we can submit at a time to retrieve their information.

* We need logic to aggregate lat and long data with the corresponding stores, but where should we put this logic? Ideally we want all data access to be abstracted away from the calling code. We could put this logic into the repository, but that would increase the responsibility of the repository since it would now be pulling data from the store file as well as data from Postcodes.io. I would rule this out as the guiding factor is to ensure maximum testability of code. A less intrusive approach is to create another repository to retrieve the lat and long information for the stores. This new repostory will use an api client under the hood to retrieve the data. Still, we want to abstract away the detail so the calling code doesn't need to know 2 repositories are at play. So the approach is to create a view, whose responsibility is to aggregate and provide the requested data to the calling code. I categorize this views module as part of a servicing layer to the calling code and will create a srv_layer folder with a views.py file inside.

#### 2.2.2) Write tests and basic implementation
* Before writing tests, I will first refactor my implementation of 2.1) and move references to the existing repository out of the route method and into views.py. Then the route method can have a direct reference to views.py.

* Now with 2.1) working again but this time referencing views.py, I can provide a draft implementation getting the lat and long information from Postcodes.io and aggregate with the stores data within views.py, again, writing the tests first. This time, we need to write some integrations test as there is a need to aggregate the data to be presented to the route method. The tests will check that the calls to retrieve lat and long data is working and that we can aggregate that data with the initial stores data. A new e2e test case is also required to make sure Lat and Long are being displayed properly.

#### 2.2.3) Refactor implementation and tests
* We will create a new repository to source lat and long information. Then our views.py will reference this object.
* At this point there are a few areas that have been identified for improvements. Firstly our integrations and e2e tests would ordinarily be OK, but in this case they are making real calls to an external api. It would be polite to the service provider if we kept these calls to a minimum. We're also seeing some instantiation of concrete repository classes inside our route endpoint methods. We need to do some refactoring in the route endpoint methods such that it no longer holds any references to concrete repositories. We can create a repo factory class that provides the methods we need to create the 2 repositories. This will begin with an interface that declares the methods we want, then implement this interface to provide creation functionalities of the 2 repositories. An alternative approach is to segregate the interface into 2 separate interfaces, one for the creation of each repo. However, as both repos are likely to be used together, it makes more sense to put them together.
* To mimic retrieving the data from Postcodes.io, we can extract all the relevant lat and long data using a one-time call, then store the resulting json into a file. We then build a FakeStorePostcodesIORepo to simply read the file to retrieve the data.


### 2.3) Build the functionality that allows you to return a list of stores in a given radius of a given postcode in the UK. The list must be ordered from north to south. No need to render anything, but the function needs to be unit tested.
* Approach
* Write tests and basic implementation
* Refactor implementation and tests


#### 2.3.1) Approach
This functionality will require domain knowledge to implement. For example, the algorithm that will be used to calculate the distance from one postcode to another is knowledge of the subject matter experts and should be classified as domain knowledge. We therefore create a "domain" folder to encapsulate domain knowledge. Domain objects exists purely to provide business logic to the application.

Having performed some research, I will be using the Havensine formula to calculate the distance between 2 points. Its important to be aware that the business may prescribe a different formula to use for this so the best practice is to check with the business first.

#### 2.3.2) Write tests and basic implementation
The domain models are the main focus in this phase. Thankfully we have only a small task, but if the domain logic gets more complicated, then this is the place to include them. Domain models must solely focus on domain - it shouldn't be concerned with data store and retrieval. Therefore, tests we write will be unit tests to thoroughly ensure domain logic works.

#### 2.3.3) Refactor implementation and tests
At this stage, there are fewer areas we can refactor, however the flask routes are currently defined the the app.py file and as the number of routes grow, we need a way to make them more managable. The approach is to create the entrypoints folder to house the routes.
During my testing I observed that there are some discrepencies between the distance calculated by the Haversine algorithm and Google's search engine results. I'm not entirely sure of the reason, but it could be that Google uses an optimized model. For our purposes, I will continue to use the Haversine formula and ensure that my implementation of this formula works as expected.
