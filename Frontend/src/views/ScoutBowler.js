import axios from 'axios';
import { useState } from "react";
// reactstrap components
import bowler from "assets/img/bowler.jpg";
import {
  Button,
  Card, CardBody, CardHeader, CardImg, CardTitle, Col, Form,
  FormGroup,
  Input, Label, Row, Table
} from "reactstrap";

function ScoutBowler(props) {

  const [showTable, setShowTable] = useState(false);
  const [shorlistedPlayers, setShorlistedPlayers] = useState([{
    name: '',
    basePrice: '',
    bowlingStyle: '',
    predictedRating: '',
    country: '',
    capStatus: '',
    description: '',
  }]);
  const [bowlingStyle, setBowlingStyle] = useState('Spin-Bowler');
  const [minPrice, setMinPrice] = useState('20');
  const [maxPrice, setMaxPrice] = useState('200');
  const [role, setRole] = useState('Bowler');

  function predictBowler() {
    axios(
      ' http://056e244df44a.ngrok.io/predictBowler', {
      method: 'POST',
      data: {
        "bowlingStyle": bowlingStyle,
        "minPrice": minPrice,
        "maxPrice": maxPrice,
        "role": role
      },
      headers: {
        'Content-Type': 'application/json'
      }
    }
    ).then(response => {
      if (response.data.statusCode === "200") {
        setShorlistedPlayers(response.data.data);
      }
    })
      .catch(error => {
        console.error('There was an error!', error);
      });

  };

  return (
    <>
      <div className="content">
        <Row>
          <Col lg="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h2">Let's identify the best wicket takers</CardTitle>
              </CardHeader>
              <CardBody>
                <Row>
                  <Col lg="4" md="6">
                    <CardImg top width="80%" src={bowler} alt="Card image cap" />
                  </Col>
                  <Col lg="8" md="6">
                    <Form>
                      <Col md={6}>
                        <FormGroup >
                          <Label for="chooseBowlingStyle" tag="h3">Choose Bowling Style</Label>
                          <Input bsSize="lg" type="select" name="bowlingStyle" id="bp" onChange={(e) => setBowlingStyle(e.target.value)}>
                            <option value="Spin-Bowler">Spin Bowler</option>
                            <option value="Fast-Bowler">Fast Bowler</option>
                          </Input>
                        </FormGroup>
                      </Col>
                      <br />

                      <Col md={6}>
                        <FormGroup >
                          <Label for="chooseRole" tag="h3">Choose Specific Role</Label>
                          <Input bsSize="lg" type="select" name="role" id="bp" onChange={(e) => setRole(e.target.value)}>
                            <option value="Bowler">None</option>
                            <option value="All-Rounder">Bowling Allrounder</option>
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
                          predictBowler();
                          setShowTable(true);
                        }
                        }
                      >
                        Show Bowlers to Target
                      </Button>
                    </Form>
                  </Col>
                </Row>
                {showTable ? <div>
                  <Col lg="12" md="12">
                    <Card>
                      <CardHeader>
                        <CardTitle tag="h2">Shortlisted Bowlers</CardTitle>
                      </CardHeader>
                      <CardBody>
                        <Table className="tablesorter" responsive>
                          <thead className="text-primary">
                            <tr>
                              <th className="text-center">S.No</th>
                              <th className="text-center">Name</th>
                              <th className="text-center">Bowling Style</th>
                              <th className="text-center">Country</th>
                              <th className="text-center">Base Price</th>
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
                                <td className="text-center">{row.bowlingStyle}</td>
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

export default ScoutBowler;
