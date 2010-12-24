 ---------------
 ZCML directives
 ---------------
<conveyor>

<first_group
	name="1"
	worker = ".class,Worker"
	worker_name = "initial_worker"
	quantity = "50"
	delay = "5"
	out_queue = ".class.Queue"
	out_queue_name = "initial_queue"
	event = ".class.Event"
	event_name ="event_"
/>

<last_group
	name="1"
	worker = ".class,Worker"
	worker_name = "initial_worker"
	quantity = "50"
	delay = "5"
	in_queue = ".class.Queue"
	in_queue_name = "initial_queue"
	event = ".class.Event"
	event_name ="event_"
/>

<group
	name="1"
	stop_order = "1"	
	worker = ".class,Worker"
	worker_name = "initial_worker"
	quantity = "50"
	delay = "5"
	in_queue = ".class.Queue"
	in_queue_name = "initial_queue"
	out_queue = ".class.Queue"
	out_queue_name = "initial_queue"
	event = ".class.Event"
	event_name ="event_"
/>