import { BackgroundColorContext } from "contexts/BackgroundColorContext";
import React from "react";
import { Redirect, Route, Switch } from "react-router-dom";
import { Nav, NavItem, NavLink } from 'reactstrap';

// core components
import routes from "routes.js";

function DCSSHome(props) {
  const getRoutes = (routes) => {
    return routes.map((prop, key) => {
      if (prop.layout === "/admin") {
        return (
          <Route
            path={prop.layout + prop.path}
            component={prop.component}
            key={key}
          />
        );
      } else {
        return null;
      }
    });
  };
  return (

    <BackgroundColorContext.Consumer>
      {() => (
        <React.Fragment>
          <div>
            <Nav>
              <NavItem>
                <NavLink href="/admin">Link</NavLink>
              </NavItem>
            </Nav>

            <Switch>
              {getRoutes(routes)}
              <Redirect from="*" to="/" />
            </Switch>
          </div>
        </React.Fragment>
      )}
    </BackgroundColorContext.Consumer>
  );
}

export default DCSSHome;
