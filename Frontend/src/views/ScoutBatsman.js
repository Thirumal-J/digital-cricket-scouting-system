import axios from 'axios';
import React, { useState } from "react";
// nodejs library that concatenates classes
import batsman from "assets/img/batsman.png";
// react plugin used to create charts
// reactstrap components
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  CardImg,
  Label,
  Form,
  FormGroup,
  Input,
  Table,
  Row,
  Col,
} from "reactstrap";

function ScoutBatsman(props) {
  const [showTable, setShowTable] = useState(false);
  const [shorlistedPlayers, setShorlistedPlayers] = useState([{
    name: '',
    basePrice: '',
    battingPosition: '',
    predictedRating: '',
    country: '',
    capStatus: '',
    description: '',
  }]);
  const [battingPosition, setBattingPosition] = useState('Top-Order-Batsman');
  const [minPrice, setMinPrice] = useState('20');
  const [maxPrice, setMaxPrice] = useState('200');
  const [role, setRole] = useState('none');

  function predictBatsman() {
    axios(
      // 'http://localhost/viewTicketUser', {
      'http://056e244df44a.ngrok.io/predictBatsman', {
      method: 'POST',
      data: {
        "battingPosition": battingPosition,
        "minPrice": minPrice,
        "maxPrice": maxPrice,
        "role": role
      },
      headers: {
        'Content-Type': 'application/json'
      }
    }
    ).then(response => {
      console.log(response.data);
      // setShorlistedPlayers(response.data)
      if (response.data.statusCode === "200") {
        console.log("inside if")
        // setParkedCarRegNo(response.data.data.ParkedCarRegNo);
        // setState({ activeTicketCount: response.data.data.length });
        if (response.data.data !== -1)
          setShorlistedPlayers(response.data.data);
      }
      else {
        // this.loginError.display = "block"
      }
    })
      .catch(error => {
        // this({ errorMessage: error.message });
        console.error('There was an error!', error);
      });

  };

  return (
    <>
      <div className="content">
        {/* <br /> */}
        <Row>
          <Col lg="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h2">Let's identify the best hitman</CardTitle>
              </CardHeader>
              <CardBody>
                <Row>
                  <Col lg="4" md="6">
                    <CardImg top width="100%" src={batsman}  alt="Card image cap" />
                  </Col>
                  <Col lg="8" md="6">
                    <Form>
                      <Col md={6}>
                        {/* <Image src={logo} roundedCircle /> */}
                      </Col>
                      <Col md={6}>
                        <FormGroup >
                          <Label for="chooseBattingPosition" tag="h3">Choose Batting Position</Label>
                          <Input bsSize="lg" type="select" name="battingPosition" id="bp" onChange={(e) => setBattingPosition(e.target.value)}>
                            <option value="Top-Order-Batsman">Top Order Batsman</option>
                            <option value="Middle-Order-Batsman">Middle Order Batsman</option>
                            <option value="Finisher-Batsman">Finisher Batsman</option>
                          </Input>
                        </FormGroup>
                      </Col>
                      <br />

                      <Col md={6}>
                        <FormGroup >
                          <Label for="chooseBattingRole" tag="h3">Choose Batsman Role</Label>
                          <Input bsSize="lg" type="select" name="battingRole" id="addOnRole" onChange={(e) => setRole(e.target.value)}>
                            <option value="none">None</option>
                            <option value="Wicket-Keeper">Wicket-Keeper</option>
                            <option value="All-Rounder">Batting All-Rounder</option>
                          </Input>
                        </FormGroup>
                      </Col>
                      <br />

                      <Col md={6}>
                        <FormGroup>
                          <Label for="chooseMinPrice" tag="h3">Minimum Price</Label>
                          <Input bsSize="lg" type="select" name="minPrice" id="minP" onChange={(e) => setMinPrice(e.target.value)}>
                            <option value="20">20 Lakhs</option>
                            <option value="50">50 Lakhs</option>
                            <option value="75">75 Lakhs</option>
                            <option value="100">1 Crore</option>
                            <option value="150">1.5 Crore</option>
                            <option value="200" >2 Crore</option>
                          </Input>
                        </FormGroup>
                      </Col>
                      <br />

                      <Col md={6}>
                        <FormGroup>
                          <Label for="chooseMaxPrice" tag="h3">Maximum Price</Label>
                          <Input bsSize="lg" type="select" name="maxPrice" id="maxP" onChange={(e) => setMaxPrice(e.target.value)}>
                            <option value="200" >2 Crore</option>
                            <option value="150">1.5 Crore</option>
                            <option value="100">1 Crore</option>
                            <option value="75">75 Lakhs</option>
                            <option value="50">50 Lakhs</option>
                            <option value="20">20 Lakhs</option>

                          </Input>
                        </FormGroup>
                      </Col>
                      <br />
                      <br />

                      <Button
                        color="info"
                        size="md"
                        onClick={(e) => {
                          predictBatsman();
                          setShowTable(true);
                        }
                        }
                      >
                        Show Batsmen to Target
                      </Button>
                    </Form>
                  </Col>
                </Row>
                {showTable ? <div>
                  <Col lg="12" md="12">
                    <Card>
                      <CardHeader>
                        <CardTitle tag="h2">Shortlisted Batsmen</CardTitle>
                      </CardHeader>
                      <CardBody>
                        <Table className="tablesorter">
                          <thead className="text-primary">
                            <tr>
                              <th className="text-center">S.No</th>
                              <th className="text-center">Name</th>
                              <th className="text-center">Batting Position</th>
                              <th className="text-center">Country</th>
                              <th className="text-center">Base Price (in Lakhs Indian Rupees)</th>
                              <th className="text-center">Capped or Uncapped</th>
                              <th className="text-center">Predicted Rating</th>
                              <th className="text-center">Predicted Performance</th>
                            </tr>
                          </thead>
                          <tbody>
                            {shorlistedPlayers.map((row, index) => (
                              <tr key={index}>
                                <td className="text-center">{index + 1}</td>
                                <td className="text-center">{row.name}</td>
                                <td className="text-center">{row.battingPosition}</td>
                                <td className="text-center">{row.country}</td>
                                <td className="text-center">{row.basePrice}</td>
                                <td className="text-center">{row.capStatus}</td>
                                <td className="text-center">{row.predictedRating}</td>
                                <td className="text-center">{row.description}</td>
                              </tr>
                            ))}
                          </tbody>
                        </Table>
                      </CardBody>
                    </Card>
                  </Col>
                </div> : null}
              </CardBody>
            </Card>
          </Col>
        </Row>


      </div>
    </>
  );
}

export default ScoutBatsman;
