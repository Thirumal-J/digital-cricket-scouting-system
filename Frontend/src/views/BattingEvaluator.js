import React, { useState } from "react";
import axios from 'axios';
import { Bar } from "react-chartjs-2";

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

function BattingEvaluator(props) {

  const [showForm, setShowForm] = useState(true);
  const [showResult, setShowResult] = useState(false);
  const [showInfoMsg, setShowInfoMsg] = useState(false);

  const [innings, setInnings] = useState('');
  const [average, setAverage] = useState('');
  const [strikeRate, setStrikeRate] = useState('');
  const [fifties, setFifties] = useState('');
  const [hundreds, setHundreds] = useState('');
  const [fours, setFours] = useState('');
  const [sixes, setSixes] = useState('');
  const [ducks, setDucks] = useState('');
  const [totalRuns, setTotalRuns] = useState('');
  const [ballsFaced, setBallsFaced] = useState('');
  const [notOuts, setNotOuts] = useState('');

  const [topOrder, setTopOrder] = useState({
    rating:3,
    Description:'Average Performer'
  });
  const [middleOrder, setMiddleOrder] = useState({
    rating:5,
    Description:'Excellent Performer'
  });
  const [finisher, setFinisher] = useState({
    rating:4,
    Description:'Good Performer'
  });

  function evaluateBatsman() {
  //   axios(
  //     'http://056e244df44a.ngrok.io/fetchRatings/batsman/1', {
  //     method: 'POST',
  //     data: {
  //       "innings": innings,
  //       "average": average,
  //       "strikeRate": strikeRate,
  //       "fifties": fifties,
  //       "hundreds": hundreds,
  //       "fours": fours,
  //       "sixes": sixes,
  //       "ducks": ducks,
  //       "totalRuns": totalRuns,
  //       "ballsFaced": ballsFaced,
  //       "notOuts": notOuts
  //     },
  //     headers: {
  //       'Content-Type': 'application/json'
  //     }
  //   }
  //   ).then(response => {
  //     console.log(response.data);
  //     // setShorlistedPlayers(response.data)
  //     // if (response.data.statusCode == "200") {
  //     //   console.log("inside if")
  //       // setParkedCarRegNo(response.data.data.ParkedCarRegNo);
  //       // setState({ activeTicketCount: response.data.data.length });
  //       if (response.data.ratings !== -1) {
  //         setTopOrder(response.data.ratings.topOrder);
  //         setMiddleOrder(response.data.ratings.middleOrder);
  //         setFinisher(response.data.ratings.finisher);
  //         setShowResult(true);
  //         setShowForm(false);
  //       }
  //       else {
  //       setShowInfoMsg(true);
  //       setShowResult(false);
  //       setShowForm(false);
  //     }
  //   })
  //     .catch(error => {
  //       // this({ errorMessage: error.message });
  //       console.error('There was an error!', error);
  //       setShowInfoMsg(true);
  //       setShowResult(false);
  //       setShowForm(false);
  //     });
          setShowResult(true);
          setShowForm(false);

  };

  

let ratingChart = {
  data: (canvas) => {
    let ctx = canvas.getContext("2d");

    let gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, "rgba(72,72,176,0.1)");
    gradientStroke.addColorStop(0.4, "rgba(72,72,176,0.0)");
    gradientStroke.addColorStop(0, "rgba(119,52,169,0)"); //purple colors

    return {
      labels: ["Top Order", "Middle Order", "Finisher"],
      datasets: [
        {
          label: "Batting Position",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: "#d048b6",
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: [topOrder.rating,middleOrder.rating, finisher.rating],
        },
      ],
    };
  },
  options: {
    maintainAspectRatio: false,
    legend: {
      display: false,
    },
    tooltips: {
      backgroundColor: "#f5f5f5",
      titleFontColor: "#333",
      bodyFontColor: "#666",
      bodySpacing: 4,
      xPadding: 12,
      mode: "nearest",
      intersect: 0,
      position: "nearest",
    },
    responsive: true,
    scales: {
      yAxes: [
        {
          gridLines: {
            drawBorder: false,
            color: "rgba(225,78,202,0.1)",
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 1,
            suggestedMax: 5,
            padding: 10,
            fontColor: "#ffffff",
          },
        },
      ],
      xAxes: [
        {
          gridLines: {
            drawBorder: false,
            color: "rgba(225,78,202,0.1)",
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#ffffff",
          },
        },
      ],
    },
  },
};
  return (
    <>
      <div className="content">
        {showForm ? <Row>
          <Col lg="12" md="12">
            <Card tag="h2">
              <CardHeader>
                <CardTitle tag="h2">Batting Performance Evaluation</CardTitle>
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
                        <Label for="average">Average</Label>
                        <Input
                          type="number"
                          name="average"
                          id="ave"
                          placeholder="What is his average?"
                          onChange={(e) => { setAverage(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="strikeRate">Strike Rate</Label>
                        <Input
                          type="number"
                          name="strikeRate"
                          id="sr"
                          placeholder="What is his career strike rate?"
                          onChange={(e) => { setStrikeRate(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                  </Row>
                  <br />
                  <br />
                  <Row form>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="fifies">Fifties</Label>
                        <Input
                          type="number"
                          name="fifties"
                          id="50s"
                          placeholder="How many 50+ runs did he score?"
                          onChange={(e) => { setFifties(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="Hundreds">Hundreds</Label>
                        <Input
                          type="number"
                          name="hundreds"
                          id="100s"
                          placeholder="How many 100+ runs did he score?"
                          onChange={(e) => { setHundreds(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="fours">Fours</Label>
                        <Input
                          type="number"
                          name="fours"
                          id="4s"
                          placeholder="How many 4s did he hit?"
                          onChange={(e) => { setFours(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                  </Row>
                  <br />
                  <br />
                  <Row form>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="sixes">Sixes</Label>
                        <Input
                          type="number"
                          name="sixes"
                          id="6s"
                          placeholder="How many 6s did he hit?"
                          onChange={(e) => { setSixes(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="ducks">Ducks</Label>
                        <Input
                          type="number"
                          name="ducks"
                          id="0s"
                          placeholder="How many times did he got out for Zero runs?"
                          onChange={(e) => { setDucks(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="totalRuns">Total Runs</Label>
                        <Input
                          type="number"
                          name="totalRuns"
                          id="runs"
                          placeholder="How many runs did he score for past one year?"
                          onChange={(e) => { setTotalRuns(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                  </Row>
                  <br />
                  <br />
                  <Row form>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="ballsFaced">Balls Faced</Label>
                        <Input
                          type="number"
                          name="ballsFaced"
                          id="bf"
                          placeholder="How many balls did he face?"
                          onChange={(e) => { setBallsFaced(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                    <Col md={4}>
                      <FormGroup>
                        <Label for="notOuts">Not Outs</Label>
                        <Input
                          type="number"
                          name="notOuts"
                          id="nos"
                          placeholder="How many innings did he remained not out?"
                          onChange={(e) => { setNotOuts(e.target.value) }}
                        />
                      </FormGroup>
                    </Col>
                  </Row>
                  <div className="text-center">
                    <Button
                      color="info"
                      size="md"
                      onClick={(e) => {
                        evaluateBatsman();
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
                <Table className="tablesorter" >
                  <thead className="text-primary">
                    <tr>
                      <th className="text-center">Batting Position</th>
                      <th className="text-center">Rating</th>
                      <th className="text-center">Predicted Performance</th>
                    </tr>
                  </thead>
                  <tbody>
                      <tr>
                        <td className="text-center">Top Order</td>
                        <td className="text-center">{topOrder.rating}</td>
                        <td className="text-center">{topOrder.Description}</td>
                      </tr>
                      <tr>
                        <td className="text-center">Middle Order</td>
                        <td className="text-center">{middleOrder.rating}</td>
                        <td className="text-center">{middleOrder.Description}</td>
                      </tr>
                      <tr>
                        <td className="text-center" >Finisher</td>
                        <td className="text-center">{finisher.rating}</td>
                        <td className="text-center">{finisher.Description}</td>
                      </tr>
                  </tbody>
                </Table>
              </CardBody>
            </Card>
          </Col>
          <Col lg="4" classname="text-center">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Rating Comparison</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-delivery-fast text-primary" />{" "}
                  
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Bar
                    data={ratingChart.data}
                    options={ratingChart.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
        </div> : null}
      </div>
    </>
  );
}

export default BattingEvaluator;
