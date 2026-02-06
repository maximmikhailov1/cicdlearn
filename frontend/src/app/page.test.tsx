import { render, screen } from "@testing-library/react";
import Home from "./page";

jest.mock("next/navigation", () => ({}));

describe("Home", () => {
  it("renders project title", async () => {
    render(<Home />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("cicdlearn");
    await screen.findByTestId("health-status");
  });

  it("renders backend health section", async () => {
    render(<Home />);
    expect(screen.getByText("Backend health")).toBeInTheDocument();
    await screen.findByTestId("health-status");
  });
});
