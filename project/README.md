Project Description
===================

This is the implementation of work-at-olist project using Django and Django Rest Framework.
The inspiration for the present archtecture was Martin Fowler's [Event Sourcin Article](https://martinfowler.com/eaaDev/EventSourcing.html).
Although some parts of the Event Sourcing capabilities are missing, this structure stablishes a good path towards them. But since it's not production grade software, some details where oversight.

the API endpoints can be foud at [api's module urls](https://github.com/romulocollopy/work-at-olist/blob/dev/project/api/urls.py), where the views and serializer are defined, using capabilities from the `apps.core` module.

The authentication used for the api was chosen on the mater of simplicity: DRF's auth token.

# Installing and testing

## Installing
```bash
$ git clone git@github.com:romulocollopy/work-at-olist.git && cd work-at-olist`
$ pipenv install
$ pipenv run project/manage.py runserver 8000
```
Optionally you can:
```bash
$ cp settings.ini.example project/settings.ini
```
and define your custom settings, as `SECRET_KEY`, `DEBUG` and `DATABASE_URL`.


## Testing
```bash
$ pipenv run project/manage.py test [module] [-n]
```

# Work Environment

This project was develop between diaper leaks, feeding and baby baths in a neat Laptop running Arch Linux version 238 with Gnome Desktop; Zsh; Emacs (and some vim); Python 3.6 and pipenv.


# API (sort of) documentation;

## Endpoints
The project demo is avaliable at https://call-records.herokuapp.com

### Token
The authentication token can be obtined with a `POST` request to https://call-records.herokuapp.com/api/token providing the `username=guest` and password `olist!guest`.

### Call Event
The call events are registered with a `POST` request to https://call-records.herokuapp.com/api/call-event/, providig the header `Authentication: Token <yourtoken>` and the body as in the project specification:

1. Call Start Record

```
{
  "id":  // Record unique identificator;
  "type":  // Indicate if it's a call "start" or "end" record;
  "timestamp":  // The timestamp of when the event occured;
  "call_id":  // Unique for each call record pair;
  "source":  // The subscriber phone number that originated the call;
  "destination":  // The phone number receiving the call.
}
```

2. Call End Record

```
{
   "id":  // Record unique identificator;
   "type":  // Indicate if it's a call "start" or "end" record;
   "timestamp":  // The timestamp of when the event occured;
   "call_id":  // Unique for each call record pair.
}
```

### Get Billing

The billing can be obtained in the with a `GET` request at https://call-records.herokuapp.com/api/call-bill/?source=AAXXXXXXXXX with the optional `<month: int>` and `<year: int>` in the querystring.
As in the other endpont, Authentication Token in required as header.

# Final Consideration and improvements needed;

During to time constraints some details became oversight and should be revied:
- the call events can occour in any order and multiple times, since the api must support different scenarions, like be called by messager brokers tasks tha does not have order garantee. But the API should return 201 when the event is created and 200 when it's updated.
- there's an event sourcing table that can be used to replay the use cases and re-create the Calls with improved business logic; but the actual replay action is not implemented;
- 404 handlers and welcome page could be implemented
- since the bill shows the `duration` field instead of start and end time, this field was preferred instead of `end_timestamp`. Neverthless, the `end_timestamp` field proved itself relevant to enable the API to receive the events in the wrong order. Some refactoring could be made to eliminate the redundance between these fields. On the other hand, having a duration field slightly increases the performance, as in the query screnario it avoids some processing for calculating it, like recomended in CQS (Command-Query Separation)


It was fun to develop =), I'll try to get back to these details when possible.
