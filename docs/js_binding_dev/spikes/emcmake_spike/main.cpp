#include <emscripten/bind.h>
#include "gluecodium/calculator/Calculator.h"
#include <memory>
#include <cstdint>
using namespace emscripten;
using gluecodium::calculator::Calculator;

class SpikeCalculator : public Calculator {
public:
    ::gluecodium::Return<int32_t, ::std::error_code>
    summarize(const int32_t first, const int32_t second) override {
        return {first + second};
    }
    void subtract(const int32_t a, const int32_t b,
                  const Calculator::SubtructCallback& callback) override {
        auto r = summarize(a, -b);
        if (r.has_value()) callback(std::nullopt, r.unsafe_value());
        else callback(static_cast<Calculator::CalculatorError>(r.error().value()), std::nullopt);
    }
    void multiply(const int32_t a, const int32_t b,
                  const std::shared_ptr<Calculator::MultiplyCallback>& cb) override {
        int64_t p = static_cast<int64_t>(a) * b;
        if (p > INT32_MAX || p < INT32_MIN)
            cb->on_error(Calculator::CalculatorError::RESULT_OUT_OF_BOUNDS);
        else cb->on_result(static_cast<int32_t>(p));
    }
    Calculator::DivideResult divide(const Calculator::DivideArguments& args) override {
        Calculator::DivideResult r; r.result = static_cast<double>(args.dividend) / args.divider; return r;
    }
    std::shared_ptr<Calculator::MinResultRetriever> min(const int32_t, const int32_t) override {
        return nullptr;
    }
    std::optional<int32_t> max(const std::optional<int32_t>& first,
                               const std::optional<int32_t>& second) override {
        if (!first) return second;
        if (!second) return first;
        return std::max(*first, *second);
    }
};

static int32_t wrapSummarize(Calculator& c, int32_t a, int32_t b) {
    auto r = c.summarize(a, b);
    return r.has_value() ? r.unsafe_value() : -1;
}

std::shared_ptr<Calculator> makeCalc() { return std::make_shared<SpikeCalculator>(); }

EMSCRIPTEN_BINDINGS(calculator) {
    class_<Calculator>("Calculator")
        .smart_ptr<std::shared_ptr<Calculator>>("Calculator")
        .function("summarize", &Calculator::summarize);
    function("makeCalculator", &makeCalc);
    function("summarizePlain", &wrapSummarize);
}
