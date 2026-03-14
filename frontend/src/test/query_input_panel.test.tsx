import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import QueryInputPanel from "../components/QueryInputPanel";

describe("QueryInputPanel", () => {
  it("disables submit until a question is entered", () => {
    const onSubmit = vi.fn();
    render(<QueryInputPanel isLoading={false} onSubmit={onSubmit} />);
    const button = screen.getByRole("button", { name: "Run Query" });
    expect(button).toBeDisabled();
  });

  it("submits the typed question", () => {
    const onSubmit = vi.fn();
    render(<QueryInputPanel isLoading={false} onSubmit={onSubmit} />);
    const input = screen.getByPlaceholderText(
      "Example: Show top 10 customers by revenue in Q1.",
    );
    fireEvent.change(input, { target: { value: "show orders" } });
    const button = screen.getByRole("button", { name: "Run Query" });
    fireEvent.click(button);
    expect(onSubmit).toHaveBeenCalledWith("show orders");
  });

  it("shows loading label when running", () => {
    const onSubmit = vi.fn();
    render(<QueryInputPanel isLoading={true} onSubmit={onSubmit} />);
    expect(screen.getByRole("button", { name: "Running..." })).toBeDisabled();
  });
});

