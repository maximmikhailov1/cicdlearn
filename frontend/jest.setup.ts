import "@testing-library/jest-dom";

globalThis.fetch = jest.fn(() =>
  Promise.resolve({ json: () => Promise.resolve({ status: "ok" }) } as Response)
);
