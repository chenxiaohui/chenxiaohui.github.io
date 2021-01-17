---
layout: article
title: "python是一门蛋疼的语言"
key: pypython-is-an-eggache-language
date: 2016-06-20 20:22
comments: true
published: true
categories: "Python"
---
  最近在分析一个问题，用python写的测试脚本里面跟store节点通信的时候加了一个starttime和超时，store判断了startime跟当前时间之间是否已经达到超时时间，如果到达就拒绝掉。这个脚本在测试case数少的时候没啥问题，数量大了之后就有超时的问题。开始直接调大了timeout让测试先过去了，最近加了多重timeout判断，不能直接为了测试改参数了，分析一下怀疑timeout只生成了一次，封包代码如下：

	def pack_packet(ver, pcode, channel, sess, data):

	    fields = (i8(ver), u16(pcode), u16(channel), u64(sess), i64(len(data)), i64(time.time()  * 1000000), u64(0), i64(8000000), u64(0), u64(0))
	    header = ''.join(fields)

	    crc = u64(crc64(header))
	    data_crc = u64(crc64(data))

	    return fields + (crc, data, data_crc)

	def req_create_replica(replica_id):
	    pc = PacketCode
	    return pack_packet(0, pc.S3_CREATE_REPLICA, 1, gen_sess_id(), replica_id)


  python是对静态对象做过优化，相同的静态对象只维护一个，但是这个看着怎么也不是静态对象。后来打日志发现封包的日志都在日志的最前面，才想起来原来这里：


	cases_normal_flow = [

    ('create secondary replica',
     req_create_replica(pack_replica_id(0x01010101, 'cp3p', 5555555)),
     recv_create_replica,
    ),

    ('write chunk with 1 record',
     lambda: req_write_chunk(last_created_replica_id(), REPLICA_HEADER, [
             (pack_record_id(0x11111111, 001, 0x55555555), t_object_id, "abcd"), ]),
     (0, [])
    ),

    ('read record written in above step',
     lambda: req_read_record(last_created_replica_id(),
                             pack_record_id(0x11111111, 001, 0x55555555)),
     (0, [pack_lstr("abcd")])
    )]

  非lambda表达式的部分已经在cases_normal_flow全局对象定义的时候执行过了，所以要么再发送的时候重新修改时间，要么都换成lambda表达式。python的灵活总让人有种错觉觉得怎么写都是对的。这部分如果在c下面，函数指针和函数执行还是泾渭分明的。当然，人生苦短，要用好python。
