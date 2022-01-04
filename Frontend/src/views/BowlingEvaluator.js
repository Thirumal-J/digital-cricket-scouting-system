import React,  { useState } from "react";
import axios from 'axios';

// reactstrap components
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  Label,
  Form,
  FormGroup,
  Input,
  Table,
  Row,
  Col,
} from "reactstrap";

function BowlingEvaluator(props) {

  const [showForm, setShowForm] = useState(true);
  const [showResult, setShowResult] = useState(false);
  const [showInfoMsg, setShowInfoMsg] = useState(false);

  const [innings, setInnings] = useState('');
  const [overs, setOvers] = useState('');
  const [wicketsTaken, setWicketsTaken] = useState('');
  const [economy, setEconomy] = useState('');
  const [maidens, setMaidens] = useState('');
  const [fourWickets, setFourWickets] = useState('');
  const [fiveWickets, setFiveWickets] = useState('');

  const [fetchedRatings, setFetchedRatings] = useState({
    rating:0,
    Description:''
  });

  const wicketTaker = "Seems good wicket taker but may leak runs";
  const defensive = "Seems more defensive bowler, can control runs than wicket taking";
  const [qualities, setQualities] = useState('');

  function updateQuality() {
    if (wicketsTaken>=15) {
      setQualities(wicketTaker);
    }
    else if (economy<=7){
      setQualities(defensive)
    }
    else {
      setQualities("He is bit unpredictable");
    }
  };
  function evaluateBowler() {
    updateQuality();
    axios(
      // 'http://localhost/viewTicketUser', {
      'http://056e244df44a.ngrok.io/fetchRatings/bowler/1', {
      method: 'POST',
      data: {
        "innings": innings,
        "overs": overs,
        "wicketsTaken ": wicketsTaken,
        "economy": economy,
        "maidens": maidens,
        "fourWickets": fourWickets,
        "fiveWickets": fiveWickets
      },
      headers: {
        'Content-Type': 'application/json'
      }
    }
    ).then(response => {
      console.log(response.data);
      // setShorlistedPlayers(response.data)
      // if (response.data.statusCode == "200") {
      //   console.log("inside if")
        // setParkedCarRegNo(response.data.data.ParkedCarRegNo);
        // setState({ activeTicketCount: response.data.data.length });
        if (response.data.ratings !== -1) {
          setFetchedRatings(response.data.ratings)
          setShowResult(true);
          setShowForm(false);
        }
        else {
        setShowInfoMsg(true);
        setShowResult(false);
        setShowForm(false);
      }
    })
      .catch(error => {
        // this({ errorMessage: error.message });
        console.error('There was an error!', error);
        setShowInfoMsg(true);
        setShowResult(false);
        setShowForm(false);
      });

  };

  return (
    <>
    <div className="content">
        {showForm ? <Row>
          <Col lg="12" md="12">
            <Card tag="h2">
              <CardHeader>
                <CardTitle tag="h2">Bowling Performance Evaluation</CardTitle>
              </CardHeader>
              <CardBody>
              <Form>
                  <Row form>
                    <Col md={4}>
                      <FormGroup>
                        <Label bsSize="lg" for="innings">Innings</Label>
                        <Input
                          type="number"
                          name="innings"
                          id="inngs"
                          placeholder="How many innings he played?"
                          onChange={(e) => { setInnings(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="oversBowled">Overs Bowled</Label>
                        <Input
                          type="number"
                          name="oversBowled"
                          id="bb"
                          placeholder="How many overs did he bowl?"
                          onChange={(e) => { setOvers(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="wicketsTaken">Wickets Taken</Label>
                        <Input
                          type="number"
                          name="wicketsTaken"
                          id="wt"
                          placeholder="How many wickets did he take?"
                          onChange={(e) => { setWicketsTaken(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                  </Row>
                  <br/>
                  <br/>
                  <Row form>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="economy">Economy</Label>
                        <Input
                          type="number"
                          name="economy"
                          id="eco"
                          placeholder="What is the economy of the bowler?"
                          onChange={(e) => { setEconomy(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="maidens">Maidens</Label>
                        <Input
                          type="number"
                          name="maidens"
                          id="mdns"
                          placeholder="How many maidens did he bowl?"
                          onChange={(e) => { setMaidens(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="fourWicketHaul">Four Wicket Haul</Label>
                        <Input
                          type="number"
                          name="fourWicketHaul"
                          id="4WicketHaul"
                          placeholder="How many 4+ wickets did he take?"
                          onChange={(e) => { setFourWickets(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                  </Row>
                  <br/>
                  <br/>
                  <Row form>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="fiveWicketHaul">Five Wicket Haul</Label>
                        <Input
                          type="number"
                          name="fiveWicketHaul"
                          id="5WicketHaul"
                          placeholder="How many 5+ wickets did he take?"
                          onChange={(e) => { setFiveWickets(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                  </Row>
                  <div className="text-center">
                    <Button
                      color="info"
                      size="md"
                      onClick={(e) => {
                        evaluateBowler();
                        // setFetchedRatings('[{"topOrderRating":3,"middleOrderRating":5,"finisherRating":4},{"topOrderRating":3,"middleOrderRating":5,"finisherRating":4}]')
                      }
                      }
                    >
                      Evaluate
                  </Button>
                  </div>
                </Form>
              </CardBody>
            </Card>
          </Col>
        </Row> : null}
        {showInfoMsg ? <div>
          <Col lg="12" md="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h2">Error occurred, try again in sometime!!</CardTitle>
              </CardHeader>
          </Card>
          </Col>
          </div>:null}
        {showResult ? <div>
          <Col lg="12" md="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h2">Predicted Performance Rating</CardTitle>
              </CardHeader>
              <CardBody>
                <Table className="tablesorter" responsive>
                  <thead className="text-primary">
                    <tr>
                      <th className="text-center">Player role</th>
                      <th className="text-center">Rating</th>
                      <th className="text-center">Predicted Performance</th>
                      <td className="text-center">Identified Qualities</td>
                    </tr>
                  </thead>
                  <tbody>
                      <tr>
                        <td className="text-center">Bowler</td>
                        <td className="text-center">{fetchedRatings.rating}</td>
                        <td className="text-center">{fetchedRatings.Description}</td>
                        <td className="text-center">{qualities}</td>
                      </tr>
                  </tbody>
                </Table>
              </CardBody>
            </Card>
          </Col>
        </div> : null}
      </div>
    </>
  );
}

export default BowlingEvaluator;
