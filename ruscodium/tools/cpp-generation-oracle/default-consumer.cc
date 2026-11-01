#include "oracle/basic/Callback.h"
#include "oracle/basic/Data.h"
#include "oracle/basic/Labels.h"
#include "oracle/basic/Worker.h"
#include <cassert>
#include <string>

int32_t oracle::basic::Worker::get_version() { return 3; }
class ConcreteWorker final : public oracle::basic::Worker {
public:
    std::string run(int32_t value) override { return std::to_string(value); }
    bool is_ready() const override { return ready; }
    void set_ready(bool value) override { ready = value; }
    std::string get_name() const override { return "worker"; }
private:
    bool ready = false;
};
int main() {
    oracle::basic::Data data("sample");
    assert(data.count == 7 && data.label == "sample" && !data.maybe);
    data.mapping.emplace("key", 9);
    assert(data.mapping.at("key") == 9);
    data.tags.insert("ready");
    assert(data.tags.count("ready") == 1);
    oracle::basic::Data::LaterAlias number = 12;
    assert(number == 12);
    ConcreteWorker worker;
    worker.set_ready(true);
    assert(worker.is_ready() && worker.run(42) == "42" && worker.get_name() == "worker");
    assert(oracle::basic::Worker::get_version() == 3);
    oracle::basic::Callback callback = [](oracle::basic::Shade) { return std::string("ok"); };
    oracle::basic::Labels labels{callback(oracle::basic::Shade::BLUE)};
    assert(labels.at(0) == "ok");
}
