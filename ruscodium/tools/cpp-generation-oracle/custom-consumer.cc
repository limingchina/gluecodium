#include "acme/api/oracle/custom/Data.h"
#include "acme/api/oracle/custom/Worker.h"
#include <cassert>
#include <memory>
#include <string>

namespace api = acme::api::oracle::custom;
class ConcreteWorker final : public api::Worker {
public:
    int32_t process(int32_t value) override { return value + 1; }
};
class ConcreteService final : public api::RenamedService {
public:
    std::string use(const std::shared_ptr<api::Worker>& worker, int32_t count) override {
        return std::to_string(worker->process(count));
    }
    int32_t get_value() const override { return value; }
    void set_value(int32_t next) override { value = next; }
private:
    int32_t value = 0;
};
int main() {
    auto worker = std::make_shared<ConcreteWorker>();
    api::RenamedService::Nested nested(17);
    api::Data data({"a", "b"}, nested, worker);
    assert(data.nested.amount == 17 && data.values.size() == 2 && data.worker->process(1) == 2);
    ConcreteService service;
    service.set_value(8);
    assert(service.get_value() == 8 && service.use(worker, 4) == "5");
}
