// Copyright (C) 2026 HERE Europe B.V.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// SPDX-License-Identifier: Apache-2.0
// License-Filename: LICENSE

#include "com/example/calculator/Calculator.h"
#include "com/example/calculator/Calculation.h"
#include "com/example/calculator/CalculationListener.h"
#include "com/example/calculator/CalculatorErrorCode.h"

#include <memory>
#include <sstream>
#include <system_error>

namespace api = com::example::calculator;

namespace {

class CalculatorImpl final : public api::Calculator {
public:
    api::Calculation add(const double left, const double right) override {
        return calculate(left, "+", right, left + right);
    }

    api::Calculation subtract(const double left, const double right) override {
        return calculate(left, "-", right, left - right);
    }

    api::Calculation multiply(const double left, const double right) override {
        return calculate(left, "*", right, left * right);
    }

    ::Return<api::Calculation, std::error_code>
    divide(const double left, const double right) override {
        if (right == 0.0) {
            return api::make_error_code(api::CalculatorErrorCode::DIVISION_BY_ZERO);
        }
        return calculate(left, "/", right, left / right);
    }

    void set_listener(const std::shared_ptr<api::CalculationListener>& listener) override {
        listener_ = listener;
    }

    int32_t get_calculation_count() const override { return calculation_count_; }
    void set_calculation_count(const int32_t value) override { calculation_count_ = value; }

private:
    api::Calculation calculate(double left, const char* operation, double right, double value) {
        std::ostringstream expression;
        expression << left << " " << operation << " " << right;
        api::Calculation result(expression.str(), value);
        ++calculation_count_;
        if (listener_) {
            listener_->on_calculated(result);
        }
        return result;
    }

    int32_t calculation_count_ = 0;
    std::shared_ptr<api::CalculationListener> listener_;
};

} // namespace

namespace com::example::calculator {

std::shared_ptr<Calculator> Calculator::create() {
    return std::make_shared<CalculatorImpl>();
}

} // namespace com::example::calculator
