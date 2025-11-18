# utils/performance.py
import time
import psutil
from functools import wraps
from typing import Dict, Any

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        
    def time_function(self, func_name: str):
        """Decorator to time function execution"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                self.metrics[func_name] = {
                    'last_execution': execution_time,
                    'avg_execution': self._update_average(func_name, execution_time)
                }
                return result
            return wrapper
        return decorator
        
    def _update_average(self, func_name: str, new_time: float) -> float:
        """Update rolling average for function execution time"""
        if f"{func_name}_times" not in self.metrics:
            self.metrics[f"{func_name}_times"] = []
            
        times = self.metrics[f"{func_name}_times"]
        times.append(new_time)
        
        # Keep only last 100 measurements
        if len(times) > 100:
            times.pop(0)
            
        return sum(times) / len(times)
        
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'function_metrics': self.metrics
        }

# Usage example
monitor = PerformanceMonitor()

class MonitoredAgent(BaseAgent):
    def __init__(self, model_name: str = "llama3.1"):
        super().__init__(model_name)
        self.monitor = monitor
        
    @monitor.time_function('chat')
    def chat(self, message: str) -> str:
        return super().chat(message)
        
    def get_performance_report(self) -> str:
        """Generate performance report"""
        metrics = self.monitor.get_system_metrics()
        
        report = [
            "Performance Report:",
            f"CPU Usage: {metrics['cpu_percent']}%",
            f"Memory Usage: {metrics['memory_percent']}%",
            f"Disk Usage: {metrics['disk_usage']}%",
            "",
            "Function Performance:"
        ]
        
        for func_name, timing in metrics['function_metrics'].items():
            if not func_name.endswith('_times'):
                report.append(f"  {func_name}: {timing['avg_execution']:.3f}s avg")
                
        return '\n'.join(report)
