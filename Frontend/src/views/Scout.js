import axios from 'axios';
import React, { useState } from "react";
import {
  Button, ButtonDropdown, ButtonGroup,
  Card, CardBody, CardHeader, CardTitle, Col, DropdownItem, DropdownMenu, DropdownToggle, FormGroup,
  Input, Label, Row
} from "reactstrap";

function Scout(props) {
  const [bigChartData, setbigChartData] = React.useState("data1");
  const setBgChartData = (name) => {
    setbigChartData(name);
  };

  const [showBatsmanOptions, setShowBatsmanOptions] = useState(false);
  const [showBowlerOptions, setShowBowlerOptions] = useState(false);
  const [showAROptions, setShowAROptions] = useState(false);
  const [rSelected, setRSelected] = useState(null);

  function predictBatsman() {
    axios(
      ' https://b6965b5ff935.ngrok.io/predictBatsman', {
      method: 'POST',
      data: {
        "battingPosition": "topOrder",
        "minPrice": "1c",
        "maxPrice": "2c"
      },
      headers: {
        'Content-Type': 'application/json'
      }
    }
    ).then(response => {
      console.log(response.data);
    })
      .catch(error => {
        console.error('There was an error!', error);
      });

  };

  const showOptions = (e) => {
    setShowBatsmanOptions(true);
    setShowBowlerOptions(false);
    setShowAROptions(false);
  }

  const [dropdownOpen, setOpen] = useState(false);

  const toggle = () => setOpen(!dropdownOpen);

  return (
    <>
      <div className="content">
        <Row>
          <Col lg="8" md="12">
            <Card>
              <CardHeader outline color="secondary">
                <CardTitle tag="h2" className="text-primary">Let's find the suitable players to target in the auction</CardTitle>
              </CardHeader>
              <CardBody tag="h5" className="">
                Choose the role of the players
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col lg="4">
            <Card className="card-chart">
              <CardBody tag="h3" className="text-center">
                <Col lg="12" >
                  <Button
                    color="info"
                    size="md"
                    onClick={(e) => showOptions(e)}
                  >
                    Batsman
                  </Button>
                </Col>
              </CardBody>
            </Card>
          </Col>
          <Col lg="6">
            <Card className="card-chart">
              {showBatsmanOptions ?
                <div><CardBody tag="h3" className="text-center text-success">
                  <h5>Select Batsman Position</h5>
                  <ButtonGroup>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Top order</Button>
                    <Button color="info" onClick={() => setRSelected(2)} active={rSelected === 2}>Middle Order</Button>
                    <Button color="info" onClick={() => setRSelected(3)} active={rSelected === 3}>Finisher</Button>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Wicket keeper</Button>
                  </ButtonGroup>
                  <FormGroup>
                    <Label for="exampleSelect">Select</Label>
                    <Input type="select" name="select" id="exampleSelect">
                      <option>20 Lakhs</option>
                      <option>50 Lakhs</option>
                      <option>75 Lakhs</option>
                      <option>1 Crore</option>
                      <option>1.5 Crore</option>
                      <option>2 Crore</option>
                    </Input>
                  </FormGroup>
                  <FormGroup>
                    <Label for="priceRange">Minimum Price</Label>
                    <Input type="range" name="range" id="priceRange" />
                  </FormGroup>
                  <ButtonDropdown isOpen={dropdownOpen} toggle={toggle}>
                    <DropdownToggle caret color="info">
                      Select Minimum Price
                    </DropdownToggle>
                    <DropdownMenu>
                      <DropdownItem>20L</DropdownItem>
                      <DropdownItem>50L</DropdownItem>
                      <DropdownItem>75L</DropdownItem>
                      <DropdownItem>1C</DropdownItem>
                      <DropdownItem>1.5C</DropdownItem>
                    </DropdownMenu>
                  </ButtonDropdown>
                </CardBody>
                </div> : null}
            </Card>
          </Col>
        </Row>
        <Row>
          <Col lg="4">
            <Card className="card-chart">
              <CardBody tag="h3" className="text-center text-success">
                <Col lg="12" className="text-center text-success">
                  <Button
                    color="info"
                    size="lg"
                    onClick={() => {
                      setShowBatsmanOptions(false);
                      setShowBowlerOptions(true);
                      setShowAROptions(false);
                    }}>
                    Bowler
                  </Button>
                </Col>
              </CardBody>
            </Card>
          </Col>
          <Col lg="8">
            <Card className="card-chart">
              {showBowlerOptions ?
                <div><CardBody tag="h3" className="text-center text-success">
                  <h5>Select Batsman Position</h5>
                  <ButtonGroup>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Top order</Button>
                    <Button color="info" onClick={() => setRSelected(2)} active={rSelected === 2}>Middle Order</Button>
                    <Button color="info" onClick={() => setRSelected(3)} active={rSelected === 3}>Finisher</Button>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Wicket keeper</Button>
                  </ButtonGroup>
                </CardBody>
                </div> : null}
            </Card>
          </Col>
        </Row>
        <Row>
          <Col lg="4">
            <Card className="card-chart">
              <CardBody tag="h3" className="text-center text-success">
                <Col lg="12" className="text-center text-success">
                  <Button
                    color="info"
                    size="lg"
                    onClick={() => {
                      setShowBatsmanOptions(false);
                      setShowBowlerOptions(false);
                      setShowAROptions(true);
                    }}>
                    All Rounder
                  </Button>
                </Col>
              </CardBody>
            </Card>
          </Col>
          <Col lg="8">
            <Card className="card-chart">
              {showAROptions ?
                <div><CardBody tag="h3" className="text-center text-success">
                  <h5>Select Batsman Position</h5>
                  <ButtonGroup>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Top order</Button>
                    <Button color="info" onClick={() => setRSelected(2)} active={rSelected === 2}>Middle Order</Button>
                    <Button color="info" onClick={() => setRSelected(3)} active={rSelected === 3}>Finisher</Button>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Wicket keeper</Button>
                  </ButtonGroup>
                </CardBody>
                </div> : null}
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Scout;
